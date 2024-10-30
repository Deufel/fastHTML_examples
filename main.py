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

from fasthtml.common import *

def make_article(title):
    """Create a sample article with lorem ipsum content"""
    return Article(
        H3(title),
        P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum nec purus tellus. Duis volutpat tellus vitae diam ultricies, quis sollicitudin eros ultricies."),
        P("Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris."),
        Button("Read more", cls="outline")
    )

def layout():
    return (
        Title('Layout'),
        Body(
            Style('''
                /* Base layout */
                me {
                    min-height: 100vh;
                    display: grid;
                    grid-template-columns: 300px minmax(300px, 800px) 300px;
                    grid-template-rows: auto 1fr auto;
                    grid-template-areas:
                        "navbar navbar navbar"
                        "aside_left main aside_right"
                        "footer footer footer";
                    grid-gap: 1rem;
                    padding: 0 max(1rem, calc((100vw - 1400px) / 2));
                }

                /* Hide sidebars when collapsed */
                me.hide-left {
                    grid-template-areas:
                        "navbar navbar navbar"
                        "main main aside_right"
                        "footer footer footer";
                }
                me.hide-right {
                    grid-template-areas:
                        "navbar navbar navbar"
                        "aside_left main main"
                        "footer footer footer";
                }
                me.hide-both {
                    grid-template-areas:
                        "navbar navbar navbar"
                        "main main main"
                        "footer footer footer";
                }

                /* Mobile adjustments */
                @media (max-width: 768px) {
                    me {
                        grid-template-columns: 1fr;
                        grid-template-areas:
                            "navbar"
                            "main"
                            "footer";
                        padding: 0;
                    }
                }
            '''),

            Nav(
                Style('''
                    me {
                        position: sticky;
                        top: 0;
                        grid-area: navbar;
                        background: var(--pico-background-color);
                        padding: 1rem;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        z-index: 101;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    }
                '''),
                H2("Layout Test"),
                Div(
                    Group(
                        Button("Toggle Left",
                            hx_post="/toggle/left",
                            hx_target="body",
                            hx_swap="classes toggle:hide-left"
                        ),
                        Button("Toggle Right",
                            hx_post="/toggle/right",
                            hx_target="body",
                            hx_swap="classes toggle:hide-right"
                        ),
                        cls="outline"
                    )
                )
            ),

            Aside(
                Style('''
                    me {
                        height: calc(100vh - 4rem);
                        top: 4rem;
                        position: sticky;
                        align-self: start;
                        grid-area: aside_left;
                        background: var(--pico-background-color);
                        padding: 1rem;
                        overflow-y: auto;
                    }
                '''),
                H3("Left Sidebar"),
                make_article("Left Article 1"),
                make_article("Left Article 2")
            ),

            Main(
                Style('''
                    me {
                        grid-area: main;
                        padding: 1rem;
                        display: flex;
                        flex-direction: column;
                        gap: 1rem;
                    }
                '''),
                *(make_article(f"Main Article {i}") for i in range(1, 6))
            ),

            Aside(
                Style('''
                    me {
                        height: calc(100vh - 4rem);
                        top: 4rem;
                        position: sticky;
                        align-self: start;
                        grid-area: aside_right;
                        background: var(--pico-background-color);
                        padding: 1rem;
                        overflow-y: auto;
                    }
                '''),
                H3("Right Sidebar"),
                make_article("Right Article 1"),
                make_article("Right Article 2")
            ),

            Footer(
                Style('''
                    me {
                        grid-area: footer;
                        padding: 1rem;
                        text-align: center;
                        background: var(--pico-background-color);
                    }
                '''),
                P("© 2024 Layout Test")
            )
        )
    )

# Toggle handlers
@rt('/toggle/{side}')
def post(side: str):
    return ""

# Home Page
@rt('/')
def get():
    return layout()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    uvicorn.run(app, host="0.0.0.0", port=port)
