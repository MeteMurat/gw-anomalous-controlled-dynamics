"""Build the complete manuscript from its canonical Markdown source.

Requires preinstalled Python, Pandoc and XeLaTeX; installs nothing and makes
no network request. Original input identities and numerical results are not
changed. HTML figure embeds/captions are normalized to printable figures.
"""
from pathlib import Path
import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess


HEADER = r'''
\usepackage{amsmath,amssymb,booktabs,longtable,array,graphicx}
\usepackage{float,caption,etoolbox,fancyhdr}
\usepackage{newunicodechar}
\newunicodechar{−}{-}
\newunicodechar{ }{\,}
\newunicodechar{ }{\,}
\newunicodechar{ }{\,}
\newunicodechar{ }{\,}
\newunicodechar{≠}{\ensuremath{\ne}}
\newunicodechar{≤}{\ensuremath{\le}}
\newunicodechar{≥}{\ensuremath{\ge}}
\newunicodechar{≈}{\ensuremath{\approx}}
\newunicodechar{×}{\ensuremath{\times}}
\newunicodechar{→}{\ensuremath{\to}}
\newunicodechar{Δ}{\ensuremath{\Delta}}
\newunicodechar{σ}{\ensuremath{\sigma}}
\newunicodechar{α}{\ensuremath{\alpha}}
\newunicodechar{ρ}{\ensuremath{\rho}}
\newunicodechar{∼}{\ensuremath{\sim}}
\setlength{\emergencystretch}{4em}
\setlength{\LTleft}{0pt}
\setlength{\LTright}{0pt}
\setlength{\tabcolsep}{4pt}
\AtBeginEnvironment{longtable}{\footnotesize\setlength{\emergencystretch}{4em}}
\captionsetup{font=small,labelfont=bf}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small Structured gravitational-wave transients}
\fancyhead[R]{\small Manuscript and scientific supplement}
\fancyfoot[C]{\thepage}
\setlength{\headheight}{14pt}
\AtBeginDocument{\hypersetup{colorlinks=true,linkcolor=blue,urlcolor=blue,breaklinks=true}}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
'''


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def plain_html(s):
    # Preserve auto-link DOI syntax and inline Markdown/math; only strip actual
    # structural HTML elements from the manuscript's existing Pandoc export.
    s = re.sub(r'<br\s*/?>', '\n', s, flags=re.I)
    s = re.sub(r'</?(?:div|span|a|em|strong|i|b|p|sup|sub)\b[^>]*>', '', s, flags=re.I)
    return html.unescape(s)


def normalize(source):
    figures = []
    counts = {}
    def figure(match):
        attrs, inside = match.group(1), match.group(2)
        image = re.search(r'<(?:img|embed)\b[^>]*\bsrc="([^"]+)"[^>]*>', inside, flags=re.I)
        cap = re.search(r'<figcaption>(.*?)</figcaption>', inside, flags=re.I|re.S)
        if not image:
            raise ValueError('FIGURE_WITHOUT_IMAGE')
        ident = re.search(r'\bid="([^"]+)"', attrs)
        label = ident.group(1) if ident else 'figure_'+str(len(figures)+1)
        counts[label] = counts.get(label,0)+1
        if counts[label]>1:
            label += '_supplement_'+str(counts[label])
        caption = plain_html(cap.group(1)) if cap else ''
        caption = re.sub(r'\s+', ' ', caption).strip()
        # Use raw LaTeX with caption content separately converted by Pandoc,
        # preserving math and avoiding Markdown bracket/link ambiguity.
        figures.append({'id':label,'path':image.group(1),'caption':caption})
        return '\n\n!['+caption+']('+image.group(1)+'){#'+label+' width=100%}\n\n'
    text = re.sub(r'<figure\b([^>]*)>(.*?)</figure>', figure, source, flags=re.I|re.S)
    text = text.replace('<div id="refs" class="references csl-bib-body hanging-indent">', '\n# References\n')
    text = plain_html(text)
    # The Markdown export carries duplicate/multiple TeX labels inside
    # unnumbered display/"aligned" math. They cannot identify equation numbers
    # in this representation and cause amsmath errors; remove label markup
    # while preserving every equation character. The source retains them.
    text = re.sub(r'\\label\{[^}]+\}', '', text)
    # Freeze display math as raw LaTeX blocks. The original export places
    # several $$ displays mid-paragraph with aligned environments, which can
    # otherwise be parsed as raw TeX outside math by Pandoc.
    text = re.sub(r'\$\$(.*?)\$\$',
                  lambda m:'\n\n```{=latex}\n\\[\n'+re.sub(r'\n\s*\n','\n',m.group(1).strip())+'\n\\]\n```\n\n',
                  text, flags=re.S)
    # Normalize typographic hyphens in prose, leaving mathematical subtraction
    # and all numbers/units in place. Unicode minus is handled by TeX above.
    for dash in ('\u2010','\u2011','\u2012','\u2013','\u2014'):
        text = text.replace(dash, '-')
    text = text.replace('\u00a0',' ').replace('\u200b','')
    # The canonical first heading is a document title rather than section1.
    lines = text.splitlines()
    title = lines[0][2:] if lines and lines[0].startswith('# ') else 'Gravitational-wave anomaly analysis'
    if lines and lines[0].startswith('# '):
        lines = lines[1:]
    body = '\n'.join(lines).lstrip()
    body = re.sub(r'^Murat Metehan Türkoğlu\s*\n', '', body, count=1)
    body = re.sub(r'^\*\*Publication narrative revision[^\n]*\n', '', body.lstrip(), count=1).lstrip()
    if body.startswith('## Abstract\n'):
        body = body[len('## Abstract\n'):]
        abstract, rest = body.split('# Introduction',1)
        # This environment is passed as raw TeX. Escape prose percent signs
        # so the remainder of a single-line abstract is not treated as a comment.
        abstract = re.sub(r'(?<!\\)%', r'\\%', abstract)
        body = '\\begin{abstract}\n'+abstract.strip()+'\n\\end{abstract}\n\n# Introduction'+rest
    body = body.replace('# Scientific supplement', '\\clearpage\n\\appendix\n# Scientific supplement',1)
    return title, body, figures


def improve_typesetting(tex):
    """Rebalance table widths and allow breaks in long inline numeric lists."""
    def table(match):
        content=match.group(0)
        fractions=[float(x) for x in re.findall(r'\\real\{([0-9.]+)\}',content)]
        if not fractions:
            return content
        minimum=min(.12,.8/len(fractions))
        excess=[max(0.,x-minimum) for x in fractions]
        total=sum(excess)
        target=[minimum+(1-len(fractions)*minimum)*x/total for x in excess] if total else [1/len(fractions)]*len(fractions)
        replacements=iter(target)
        return re.sub(r'\\real\{[0-9.]+\}',lambda _:r'\real{'+format(next(replacements),'.6f')+'}',content)
    tex=re.sub(r'\\begin\{longtable\}.*?\\toprule',table,tex,flags=re.S)
    tex=re.sub(r'\\\((.*?)\\\)',lambda m:r'\('+re.sub(r',(?!\\allowbreak)',r',\\allowbreak ',m.group(1))+r'\)',tex,flags=re.S)
    # Long SHA256 strings and provenance filenames must remain exact but
    # need legal line-break positions, especially in narrow table columns.
    def inline_code(match):
        value=match.group(1)
        if re.fullmatch(r'[A-Fa-f0-9]{64}',value):
            return r'\allowbreak'.join(r'\texttt{'+value[i:i+8]+'}' for i in range(0,64,8))
        if len(value)>30:
            value=value.replace(r'\_',r'\_\allowbreak ')
        return r'\texttt{'+value+'}'
    tex=re.sub(r'\\texttt\{([^{}]+)\}',inline_code,tex)
    return tex


def build(source, output, build_dir):
    source, output, build_dir = Path(source).resolve(), Path(output).resolve(), Path(build_dir).resolve()
    if not source.is_file():
        raise FileNotFoundError('CANONICAL_MANUSCRIPT_MISSING:'+str(source))
    for program in ('pandoc','xelatex'):
        if not shutil.which(program):
            raise RuntimeError('PREINSTALLED_PROGRAM_REQUIRED:'+program)
    build_dir.mkdir(parents=True,exist_ok=True)
    output.parent.mkdir(parents=True,exist_ok=True)
    original = source.read_text(encoding='utf-8')
    title, body, figures = normalize(original)
    roots=(source.parent,source.parent.parent)
    figure_root=next((r for r in roots if all((r/f['path']).is_file() for f in figures)),None)
    if figure_root is None:
        raise FileNotFoundError('MANUSCRIPT_FIGURES_MISSING: expected relative to manuscript or repository root')
    normalized = build_dir/'manuscript_normalized.md'
    normalized.write_text(body,encoding='utf-8')
    (build_dir/'header.tex').write_text(HEADER,encoding='utf-8')
    tex = build_dir/'GW_TECHNOSIGNATURES_COMPLETE.tex'
    cmd = ['pandoc',str(normalized),'--from=markdown+tex_math_dollars+raw_tex+implicit_figures',
           '--to=latex','--standalone','--number-sections','--top-level-division=section',
           '--resource-path='+os.pathsep.join(str(r) for r in roots), '--include-in-header='+str(build_dir/'header.tex'),
           '-V','documentclass=article','-V','classoption=11pt,a4paper',
           '-V','geometry:margin=22mm','-V','mainfont=Latin Modern Roman','-V','sansfont=Latin Modern Sans',
           '-V','monofont=Latin Modern Mono',
           '-M','title='+title,'-M','author=Murat Metehan Türkoğlu',
           '-M','date=1 November 2026','--output='+str(tex)]
    conversion = subprocess.run(cmd,cwd=source.parent,text=True,capture_output=True)
    (build_dir/'pandoc.log').write_text(conversion.stdout+'\n'+conversion.stderr,encoding='utf-8')
    if conversion.returncode:
        raise RuntimeError('PANDOC_FAILED; see '+str(build_dir/'pandoc.log'))
    tex.write_text(improve_typesetting(tex.read_text(encoding='utf-8')),encoding='utf-8')
    # Keep figure paths portable in the TeX output. Compile in source dir while
    # writing auxiliary files only to the separate build directory.
    compile_logs = []
    for iteration in range(2):
        run = subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',
                              '-output-directory='+str(build_dir),str(tex)],
                             cwd=figure_root,text=True,capture_output=True)
        compile_logs.append(run.stdout+'\n'+run.stderr)
        log_path = build_dir/('xelatex_run_'+str(iteration+1)+'.log')
        log_path.write_text(compile_logs[-1],encoding='utf-8')
        if run.returncode:
            raise RuntimeError('XELATEX_FAILED; see '+str(log_path))
    built = tex.with_suffix('.pdf')
    shutil.copyfile(built,output)
    report={'schema':'GW_CANONICAL_MANUSCRIPT_PDF_BUILD_V1','source_sha256':sha(source),
            'source_bytes':source.stat().st_size,'output_sha256':sha(output),
            'output_bytes':output.stat().st_size,'figures':figures,
            'figure_occurrences':len(figures),'unique_figure_files':len({f['path'] for f in figures}),
            'network_requests':0,'new_scientific_computations':0,
            'source':str(source),'output':str(output),'tex':str(tex),
            'canonical_text_preserved':True,'visual_QA_completed':False}
    (build_dir/'BUILD_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    here=Path(__file__).resolve().parent
    ap.add_argument('--source',type=Path,default=here/'01_MANUSCRIPT_CORE_DRAFT_EN.md')
    ap.add_argument('--output',type=Path,default=here/'GW_TECHNOSIGNATURES_COMPLETE_20261030.pdf')
    ap.add_argument('--build-dir',type=Path,default=here/'build')
    args=ap.parse_args()
    print(json.dumps(build(args.source,args.output,args.build_dir),ensure_ascii=False,indent=2))
