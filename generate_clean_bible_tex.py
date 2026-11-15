import re
import os

def clean_latex_text(text):
    # Escape special LaTeX characters not part of commands
    # Protect existing commands
    # We will do standard markdown conversions
    
    # Remove raw markdown tables/links for simpler TeX handling or format them
    # Convert headers
    lines = text.split('\n')
    out_lines = []
    in_itemize = False
    in_verbatim = False
    
    for line in lines:
        stripped = line.strip()
        
        # Check code block
        if stripped.startswith('```'):
            if in_verbatim:
                out_lines.append(r'\end{verbatim}')
                in_verbatim = False
            else:
                if in_itemize:
                    out_lines.append(r'\end{itemize}')
                    in_itemize = False
                out_lines.append(r'\begin{verbatim}')
                in_verbatim = True
            continue
            
        if in_verbatim:
            out_lines.append(line)
            continue
            
        # Horizontal rules
        if re.match(r'^-{3,}$', stripped) or re.match(r'^\*{3,}$', stripped):
            if in_itemize:
                out_lines.append(r'\end{itemize}')
                in_itemize = False
            out_lines.append(r'\bigskip\hrule\bigskip')
            continue
            
        # Headers
        if stripped.startswith('# '):
            if in_itemize:
                out_lines.append(r'\end{itemize}')
                in_itemize = False
            title = stripped[2:].strip()
            out_lines.append(f'\\chapter{{{title}}}')
            continue
        elif stripped.startswith('## '):
            if in_itemize:
                out_lines.append(r'\end{itemize}')
                in_itemize = False
            title = stripped[3:].strip()
            # Clean emoji
            title = re.sub(r'[^\w\s\(\)\:\,\.\-\'\"]+', '', title).strip()
            out_lines.append(f'\\section{{{title}}}')
            continue
        elif stripped.startswith('### '):
            if in_itemize:
                out_lines.append(r'\end{itemize}')
                in_itemize = False
            title = stripped[4:].strip()
            title = re.sub(r'[^\w\s\(\)\:\,\.\-\'\"]+', '', title).strip()
            out_lines.append(f'\\subsection{{{title}}}')
            continue
        elif stripped.startswith('#### '):
            if in_itemize:
                out_lines.append(r'\end{itemize}')
                in_itemize = False
            title = stripped[5:].strip()
            title = re.sub(r'[^\w\s\(\)\:\,\.\-\'\"]+', '', title).strip()
            out_lines.append(f'\\subsubsection{{{title}}}')
            continue
            
        # Lists
        m_list = re.match(r'^(\s*)[-\*]\s+(.*)$', line)
        if m_list:
            if not in_itemize:
                out_lines.append(r'\begin{itemize}')
                in_itemize = True
            item_text = m_list.group(2)
            out_lines.append(f'  \\item {item_text}')
            continue
        else:
            if in_itemize and stripped == '':
                # empty line in list or after list
                pass
            elif in_itemize and not stripped.startswith(('\\item', ' ')):
                out_lines.append(r'\end{itemize}')
                in_itemize = False

        # Blockquotes
        if stripped.startswith('> '):
            quote = stripped[2:].strip()
            out_lines.append(f'\\begin{{quote}}\\textit{{{quote}}}\\end{{quote}}')
            continue
            
        out_lines.append(line)
        
    if in_itemize:
        out_lines.append(r'\end{itemize}')
    if in_verbatim:
        out_lines.append(r'\end{verbatim}')
        
    content = '\n'.join(out_lines)
    
    # Bold & italics
    content = re.sub(r'\*\*([^*]+)\*\*', r'\\textbf{\1}', content)
    content = re.sub(r'(?<!\\)\*([^*\n]+)\*', r'\\textit{\1}', content)
    
    # Spanish em-dash
    content = re.sub(r'—', r'---', content)
    
    # Fix percent & ampersand & hash outside of commands
    # Replace lone %
    content = re.sub(r'(?<!\\)%', r'\%', content)
    # Replace lone &
    content = re.sub(r'(?<!\\)&', r'\&', content)
    # Replace lone #
    content = re.sub(r'(?<!\\)#', r'\#', content)
    
    # Clean markdown links [text](#anchor) -> text
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
    
    # Clean checkmarks [x] and [ ]
    content = content.replace('[x]', r'$\boxtimes$')
    content = content.replace('[ ]', r'$\square$')
    
    # Clean degrees
    content = content.replace('°', r'$^\circ$')
    content = content.replace('~', r'$\sim$')
    
    header = r'''\documentclass[11pt,a4paper]{report}
\usepackage[utf8]{inputenc}
\usepackage[spanish,es-nodecimaldot]{babel}
\usepackage[margin=2.5cm]{geometry}
\usepackage{setspace}
\onehalfspacing
\usepackage{charter}
\usepackage{amssymb}
\usepackage{hyperref}
\usepackage{bookmark}

\title{\textbf{BIBLIA DEL UNIVERSO}\\[0.5cm]\large El Velo Gravitacional --- Documento Canónico}
\author{Carlos G. Ramírez}
\date{Versión Canónica v1.3}

\begin{document}
\maketitle
\tableofcontents
\newpage
'''
    footer = r'''
\end{document}
'''
    return header + content + footer

if __name__ == '__main__':
    base_dir = r'C:\Users\hp\aivideogen\aivideogen\el_velo_gravitacional'
    md_path = os.path.join(base_dir, 'biblia_del_universo.md')
    tex_path = os.path.join(base_dir, 'BIBLIA_DEL_UNIVERSO.tex')
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    tex_text = clean_latex_text(md_text)
    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write(tex_text)
    print("Cleaned BIBLIA_DEL_UNIVERSO.tex generated.")
