import os
import os.path as P
import pyquery
import jinja2
import markdown
import shutil

ROOT      = P.dirname(P.abspath(__file__))
DOCFILE   = 'docs.md'
TEMPLATE  = 'index.html'
BUILDDIR  = P.join(ROOT,'build')
STATICDIR = P.join(ROOT,'static')
STATIC_TARGET = P.join(BUILDDIR,'static')
TARGET    = P.join(BUILDDIR,'index.html')

# Step 1 - Render markdown
def render_markdown(fpath):
    md = markdown.Markdown( extensions = ['meta','codehilite','tables','toc'] )
    with open(fpath, 'r') as mdfile:
        html = md.convert(mdfile.read())
    return (html, md)

# Step 2 - Generate table of contents from markdown output
def render_toc(html):
    q       = pyquery.PyQuery(html)
    elems   = q('h1,h2,h3,h4,h5,h6')
    curlvl  = -1
    out = ''
    depth = 1
    for i, e in enumerate(elems):
        lvl = int(e.tag[-1])
        if lvl == curlvl:
            out += "<li><a href='#%s'>" % e.attrib['id'] + e.text + "</a></li>\n"
        elif lvl > curlvl:
            # push ul
            depth += 1
            curlvl = lvl
            out += "<ul>\n"
            out += "<li><a href='#%s'>" % e.attrib['id'] + e.text + "</a></li>\n"
        elif lvl <  curlvl:
            # pop ul
            depth -= 1
            curlvl = lvl
            out += "</ul>\n"
            out += "<li><a href='#%s'>" % e.attrib['id'] + e.text + "</a></li>\n"
    out += "</ul>\n"*depth
    return out
        

# Step 3 - Insert markdown output & toc into jinja template
def render_jinja(fpath, content, toc=None):
    with open(fpath,'r') as tpl:
        template = jinja2.Template(tpl.read())
    return template.render(content=content, toc=toc)
    
def main():
    html, md = render_markdown(DOCFILE)
    toc = render_toc(html)
    html = render_jinja(TEMPLATE, content=html, toc=toc)
    
    # create build dir
    if not P.exists(BUILDDIR):
        os.mkdir(BUILDDIR)
    
    # copy in all static files
    if not P.exists(STATIC_TARGET):
        shutil.copytree(STATICDIR, STATIC_TARGET)
    
    with open(TARGET,'w') as out:
        out.write(html)
    
if __name__ == '__main__':
    main()
    
