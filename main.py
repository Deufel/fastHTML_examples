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

# Layout Styles
layout_styles = Style('''
    /* Define view transition animations */
    @keyframes fade-in {
        from { opacity: 0; }
    }

    @keyframes fade-out {
        to { opacity: 0; }
    }

    @keyframes slide-from-left {
        from { transform: translateX(-100%); }
    }

    @keyframes slide-from-right {
        from { transform: translateX(100%); }
    }

    /* Define view transitions */
    ::view-transition-old(sidebar-left) {
        animation: 90ms cubic-bezier(0.4, 0, 1, 1) both fade-out,
                 300ms cubic-bezier(0.4, 0, 0.2, 1) both slide-from-left;
    }
    ::view-transition-new(sidebar-left) {
        animation: 210ms cubic-bezier(0, 0, 0.2, 1) 90ms both fade-in,
                 300ms cubic-bezier(0.4, 0, 0.2, 1) both slide-from-left;
    }

    ::view-transition-old(sidebar-right) {
        animation: 90ms cubic-bezier(0.4, 0, 1, 1) both fade-out,
                 300ms cubic-bezier(0.4, 0, 0.2, 1) both slide-from-right;
    }
    ::view-transition-new(sidebar-right) {
        animation: 210ms cubic-bezier(0, 0, 0.2, 1) 90ms both fade-in,
                 300ms cubic-bezier(0.4, 0, 0.2, 1) both slide-from-right;
    }

    /* Bind transitions to classes */
    .sidebar-left { view-transition-name: sidebar-left; }
    .sidebar-right { view-transition-name: sidebar-right; }

    /* Base Layout */
    body {
        display: grid;
        min-height: 100vh;
        grid-template-areas:
            "nav"
            "main"
            "footer";
        grid-template-rows: auto 1fr auto;
        gap: var(--pico-spacing);
    }

    /* Sidebars */
    .sidebar {
        position: fixed;
        top: var(--pico-nav-height, 4rem);
        height: calc(100vh - var(--pico-nav-height, 4rem));
        width: min(300px, 80vw);
        background: var(--pico-background-color);
        padding: var(--pico-spacing);
        z-index: 90;
    }

    .aside-left {
        left: 0;
        transform: translateX(-100%);
    }

    .aside-right {
        right: 0;
        transform: translateX(100%);
    }

    .sidebar.visible {
        transform: translateX(0);
    }

    /* Desktop Layout */
    @media (min-width: 769px) {
        body {
            grid-template-areas:
                "nav    nav    nav"
                "left  main   right"
                "footer footer footer";
            grid-template-columns: 300px minmax(300px, 800px) 300px;
            padding: 0 max(var(--pico-spacing), calc((100vw - 1400px) / 2));
        }

        .sidebar {
            position: static;
            transform: none;
            height: auto;
        }

        .sidebar-toggle {
            display: none;
        }
    }
''')

hdrs=(css_scope_inline_script,css_debug, layout_styles)


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
    return Article(
        H4(title),
        P("Sample content using PicoCSS Article component"),
        footer=Small("Footer text")
    )

@rt('/')
def get():
    return (
        Title('View Transitions Demo'),
        Nav(
            Div(
                {'class': 'container'},
                Button("☰",
                    cls='outline sidebar-toggle',
                    hx_post="/toggle/left",
                    hx_target="#left-sidebar",
                    hx_swap="outerHTML transition:true"
                ),
                H2("Demo"),
                Button("☰",
                    cls='outline sidebar-toggle',
                    hx_post="/toggle/right",
                    hx_target="#right-sidebar",
                    hx_swap="outerHTML transition:true"
                ),
            )
        ),

        # Left Sidebar
        Aside(
            {'id': 'left-sidebar', 'class': 'sidebar aside-left sidebar-left'},
            H3("Left Menu"),
            Nav(
                Ul(
                    Li(A("Home", href="#")),
                    Li(A("About", href="#")),
                    Li(A("Contact", href="#"))
                )
            )
        ),

        # Main Content
        Main(
            {'class': 'container'},
            *(make_article(f"Article {i}") for i in range(1,4))
        ),

        # Right Sidebar
        Aside(
            {'id': 'right-sidebar', 'class': 'sidebar aside-right sidebar-right'},
            H3("Right Panel"),
            make_article("Side Content")
        ),

        Footer(
            {'class': 'container'},
            P("© 2024 Demo")
        )
    )

@rt('/toggle/{side}')
def post(side: str):
    """Toggle sidebar visibility with view transitions"""
    sidebar_id = f"{side}-sidebar"
    sidebar_class = f"sidebar-{side}"

    # Get current classes
    base_classes = ['sidebar', f'aside-{side}', sidebar_class]

    # Toggle visible class
    if 'visible' in request.form:
        classes = base_classes
    else:
        classes = base_classes + ['visible']

    return Aside(
        {'id': sidebar_id, 'class': ' '.join(classes)},
        H3(f"{side.title()} Panel"),
        Nav(
            Ul(
                Li(A("Home", href="#")),
                Li(A("About", href="#")),
                Li(A("Contact", href="#"))
            )
        ) if side == 'left' else make_article("Side Content")
    )



if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    uvicorn.run(app, host="0.0.0.0", port=port)
