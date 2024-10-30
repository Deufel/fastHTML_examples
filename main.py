from fasthtml.common import *
import os
from starlette.responses import PlainTextResponse  # Add this import

css_scope_inline_script = Script(r'''
window.cssScopeCount ??= 1
window.cssScope ??= new MutationObserver(mutations => {
    document?.body?.querySelectorAll('style:not([ready])').forEach(node => {
        var scope = 'me__'+(window.cssScopeCount++)
        node.parentNode.classList.add(scope)
        node.textContent = node.textContent
        .replace(/(?:^|\.|(\s|[^a-zA-Z0-9\-\_]))(me|this|self)(?![a-zA-Z])/g, '$1.'+scope)
        .replace(/((@keyframes|animation:|animation-name:)[^{};]*)\.me__/g, '$1me__')
        .replace(/(?:@media)\s(xs-|sm-|md-|lg-|xl-|sm|md|lg|xl|xx)/g,
            (match, part1) => { return '@media '+({'sm':'(min-width: 640px)','md':'(min-width: 768px)', 'lg':'(min-width: 1024px)', 'xl':'(min-width: 1280px)', 'xx':'(min-width: 1536px)', 'xs-':'(max-width: 639px)', 'sm-':'(max-width: 767px)', 'md-':'(max-width: 1023px)', 'lg-':'(max-width: 1279px)', 'xl-':'(max-width: 1535px)'}[part1]) }
        )
        node.setAttribute('ready', '')
    })
}).observe(document.documentElement, {childList: true, subtree: true})
''')

# CSS Debugging
css_debug = Style('*, *::before, *::after {box-sizing: border-box; outline:1px solid lime;}')


hdrs=(css_scope_inline_script,css_debug)


exception_handlers={
    404: lambda req, exc: Titled("404: I don't exist!"),
    418: lambda req, exc: Titled("418: I'm a teapot!")
}

app,rt = fast_app(pico=True,exception_handlers=exception_handlers, hdrs=hdrs)

# Add health check route
@rt("/health")
def get():
    # Return plain text "OK" with 200 status code
    return PlainTextResponse("OK", status_code=200)



@rt("/")
def get():
    layout = Div(
        Header(
            Hgroup(
                H1("Site Title"),
                H2("A holy grail layout using PicoCSS")
            ),
            cls="container"
        ),
        Nav(
            Ul(
                Li(A("Navigation 1", href="#", role="button")),
                Li(A("Navigation 2", href="#", role="button")),
                Li(A("Navigation 3", href="#", role="button"))
            ),
            cls="container"
        ),
        Main(
            Article(
                H3("Main Content"),
                P("This is the main content area...")
            ),
            cls="container"
        ),
        Aside(
            Article(
                H4("Sidebar"),
                P("Secondary content or additional navigation can go here.")
            ),
            cls="container"
        ),
        Footer(
            P("Footer content here"),
            cls="container"
        ),
        cls="holy-grail"
    )

    return (
        Style("""
            .holy-grail { display: grid; min-height: 100vh;
                grid-template-areas: "header" "nav" "main" "aside" "footer"; }
            @media (min-width: 768px) {
                .holy-grail { grid-template-columns: 200px 1fr 200px;
                    grid-template-areas: "header header header"
                                       "nav    main   aside"
                                       "footer footer footer"; }
            }
            header { grid-area: header; }
            nav { grid-area: nav; }
            main { grid-area: main; }
            aside { grid-area: aside; }
            footer { grid-area: footer; }
            .container { padding: var(--spacing); }
        """),
        layout
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    uvicorn.run(app, host="0.0.0.0", port=port)
