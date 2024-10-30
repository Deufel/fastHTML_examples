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


def make_article(title):
    """Helper to create sample article content using PicoCSS article component"""
    return Article(
        H4(title),
        P("Sample content using PicoCSS Article component"),
        footer=Small("Footer text")
    )

@rt('/')
def get():
    """Main layout handler"""
    return (
        Title('Responsive Layout'),
        Body(
            Style('''
                /* Base mobile-first styles */
                me {
                    display: grid;
                    min-height: 100vh;
                    grid-template-areas:
                        "nav"
                        "main"
                        "footer";
                    grid-template-rows: auto 1fr auto;
                    gap: var(--pico-spacing);
                    background: var(--pico-background-color);
                }

                /* Sidebar base styles */
                me .sidebar {
                    position: fixed;
                    top: var(--pico-nav-height, 4rem);
                    height: calc(100vh - var(--pico-nav-height, 4rem));
                    width: min(300px, 80vw);
                    background: var(--pico-background-color);
                    padding: var(--pico-spacing);
                    z-index: 90;
                    overflow-y: auto;
                    transition: transform 0.3s var(--pico-transition-timing, ease);
                }

                /* Position sidebars off-screen by default on mobile */
                me .aside_left {
                    left: 0;
                    transform: translateX(-100%);
                    border-right: var(--pico-border-width) solid var(--pico-muted-border-color);
                }

                me .aside_right {
                    right: 0;
                    transform: translateX(100%);
                    border-left: var(--pico-border-width) solid var(--pico-muted-border-color);
                }

                /* Show sidebar when active */
                me .sidebar.active {
                    transform: translateX(0);
                    box-shadow: var(--pico-card-box-shadow);
                }

                /* Desktop layout */
                @media (min-width: 769px) {
                    me {
                        grid-template-areas:
                            "nav    nav    nav"
                            "left  main   right"
                            "footer footer footer";
                        grid-template-columns: 300px minmax(300px, 800px) 300px;
                        padding: 0 max(var(--pico-spacing), calc((100vw - 1400px) / 2));
                    }

                    me .sidebar {
                        position: static;
                        transform: none;
                        height: auto;
                        box-shadow: none;
                        border: var(--pico-border-width) solid var(--pico-muted-border-color);
                        border-radius: var(--pico-border-radius);
                    }

                    /* Hide toggle buttons on desktop */
                    me .sidebar-toggle {
                        display: none;
                    }
                }

                /* Navigation styles */
                me nav {
                    position: sticky;
                    top: 0;
                    grid-area: nav;
                    background: var(--pico-background-color);
                    padding: var(--pico-spacing);
                    z-index: 100;
                    border-bottom: var(--pico-border-width) solid var(--pico-muted-border-color);
                }

                me .nav-content {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }

                /* Main content area */
                me main {
                    grid-area: main;
                    padding: var(--pico-spacing);
                    display: flex;
                    flex-direction: column;
                    gap: var(--pico-spacing);
                }

                /* Footer styles */
                me footer {
                    grid-area: footer;
                    padding: var(--pico-spacing);
                    text-align: center;
                    border-top: var(--pico-border-width) solid var(--pico-muted-border-color);
                }
            '''),

            # Navigation
            Nav(Ul(Li(Img(src='static/logo.png', alt="EventOS", width="150", height="auto"))),
                Ul( Li(Button(get_icon('login'),"Sign In", hx_get="/login", hx_target="body", hx_push_url="true", cls="outline")),
                    Li(Button(get_icon('register'),"Register", hx_get="/register", hx_target="body", hx_push_url="true", cls="outline contrast")),
                    cls="container"
            ),

            # Left Sidebar
            Aside(
                {'id': 'left-sidebar', 'class': 'sidebar aside_left'},
                H3("Left Sidebar"),
                Nav(
                    Ul(
                        Li(A("Home", href="#")),
                        Li(A("About", href="#")),
                        Li(A("Contact", href="#"))
                    )
                ),
                make_article("Left Content")
            ),

            # Main Content
            Main(
                *(make_article(f"Main Article {i}") for i in range(1, 4))
            ),

            # Right Sidebar
            Aside(
                {'id': 'right-sidebar', 'class': 'sidebar aside_right'},
                H3("Right Sidebar"),
                make_article("Right Content")
            ),

            # Footer
            Footer(
                P("© 2024 Layout Demo", cls="text-center")
            )
        )
    )

@rt('/toggle/{side}')
def post(side: str):
    """Toggle sidebar active state"""
    # This handler just toggles the 'active' class
    # HTMX will handle the class swap automatically
    return "active"



if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    uvicorn.run(app, host="0.0.0.0", port=port)
