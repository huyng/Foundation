import jinja2
import markdown

DOCFILE = 'docs.md'
TEMPLATE = 'index.jhtml'
TARGET = 'index.html'

def render_markdown(fpath):
    md = markdown.Markdown( extensions = ['meta','codehilite','tables','toc'] )
    with open(fpath, 'r') as mdfile:
        html = md.convert(mdfile.read())
    return (html, md)

def render_jinja(fpath, content):
    with open(fpath,'r') as tpl:
        template = jinja2.Template(tpl.read())
    return template.render(content=content)
    
def main():
    html, md = render_markdown(DOCFILE)
    html = render_jinja(TEMPLATE, content=html)
    with open(TARGET,'w') as out:
        out.write(html)
    
if __name__ == '__main__':
    main()
    