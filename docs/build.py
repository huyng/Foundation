import pyquery
import jinja2
import markdown

DOCFILE  = 'docs.md'
TEMPLATE = 'index.jhtml'
TARGET   = 'index.html'

def render_markdown(fpath):
    md = markdown.Markdown( extensions = ['meta','codehilite','tables','toc'] )
    with open(fpath, 'r') as mdfile:
        html = md.convert(mdfile.read())
    return (html, md)

def render_jinja(fpath, content, toc=None):
    with open(fpath,'r') as tpl:
        template = jinja2.Template(tpl.read())
    return template.render(content=content, toc=toc)

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
            out += "<li><a href='#%s'>" % e.attrib['id'] + e.text + "</a></li>\n"
            out += "</ul>\n"

    out += "</ul>\n"*depth
    return out
        
    
def main():
    html, md = render_markdown(DOCFILE)
    toc = render_toc(html)
    html = render_jinja(TEMPLATE, content=html, toc=toc)
    with open(TARGET,'w') as out:
        out.write(html)
    
if __name__ == '__main__':
    main()
    
