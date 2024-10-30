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

def layout():
    return (
        Title('Layout'),
        Body(
            Style('''
                /* Base layout */
                me {
                    min-height: 100vh;
                    display: grid;
                    grid-template-columns: 1fr 300px minmax(300px, 800px) 300px 1fr;
                    grid-template-rows: auto 1fr auto;
                    grid-template-areas:
                        "navbar navbar navbar navbar navbar"
                        "padding_left aside_left main aside_right padding_right"
                        "footer footer footer footer footer";
                    grid-gap: 1rem;
                }

                /* Desktop with less padding */
                @media (max-width: 1600px) {
                    me {
                        grid-template-columns: 20px 300px minmax(300px, 800px) 300px 20px;
                    }
                }

                /* Tablet - no padding */
                @media (max-width: 1200px) {
                    me {
                        grid-template-columns: 300px minmax(300px, 800px) 300px;
                        grid-template-areas:
                            "navbar navbar navbar"
                            "aside_left main aside_right"
                            "footer footer footer";
                    }
                }

                /* Mobile */
                @media (max-width: 768px) {
                    me {
                        grid-template-columns: 1fr;
                        grid-template-areas:
                            "navbar"
                            "main"
                            "footer";
                    }

                    me .aside_left,
                    me .aside_right {
                        position: fixed;
                        top: 4rem;
                        bottom: 0;
                        width: 300px;
                        background: white;
                        transition: transform 0.3s ease;
                        z-index: 100;
                    }

                    me .aside_left {
                        left: 0;
                        transform: translateX(-100%);
                    }

                    me .aside_right {
                        right: 0;
                        transform: translateX(100%);
                    }

                    me .aside_left.show { transform: translateX(0); }
                    me .aside_right.show { transform: translateX(0); }
                }
            '''),

            # Navigation with toggle buttons for mobile
            Nav(
                Style('''
                    me {
                        position: sticky;
                        top: 0;
                        grid-area: navbar;
                        background: white;
                        padding: 1rem;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        z-index: 101;
                    }

                    @media (min-width: 769px) {
                        me .mobile-toggles { display: none; }
                    }
                '''),
                Div('Layout Test Builder'),
                # Mobile toggle buttons
                Div(
                    {'class': 'mobile-toggles'},
                    Button('☰ Left',
                        hx_post='/toggle-left',
                        hx_target='.aside_left',
                        hx_swap='classes toggle:show'
                    ),
                    Button('Right ☰',
                        hx_post='/toggle-right',
                        hx_target='.aside_right',
                        hx_swap='classes toggle:show'
                    )
                )
            ),

            # Left padding (only shows on very wide screens)
            Div(Style('me { grid-area: padding_left; }'), {'class': 'padding_left'}),

            # Left sidebar
            Aside(
                Style('''
                    me {
                        height: calc(100vh - 4rem);
                        top: 4rem;
                        position: sticky;
                        align-self: start;
                        grid-area: aside_left;
                        background: white;
                        padding: 1rem;
                        overflow-y: auto;
                    }
                '''),
                {'class': 'aside_left'},
                'This is a Left aside'
            ),

            # Main content
            Main(
                Style('''
                    me {
                        grid-area: main;
                        padding: 1rem;
                    }
                '''),
                H1('Main'),
                P('This is the main content')
            ),

            # Right sidebar
            Aside(
                Style('''
                    me {
                        height: calc(100vh - 4rem);
                        top: 4rem;
                        position: sticky;
                        align-self: start;
                        grid-area: aside_right;
                        background: white;
                        padding: 1rem;
                        overflow-y: auto;
                    }
                '''),
                {'class': 'aside_right'},
                'This is a Right aside'
            ),

            # Right padding (only shows on very wide screens)
            Div(Style('me { grid-area: padding_right; }'), {'class': 'padding_right'}),

            # Footer
            Footer(
                Style('''
                    me {
                        grid-area: footer;
                        padding: 1rem;
                        text-align: center;
                    }
                '''),
                'Footer'
            )
        )
    )

# Routes for the toggle buttons
@rt('/toggle-left')
def post():
    return ''

@rt('/toggle-right')
def post():
    return ''

# Home Page
@rt('/')
def get():
    return layout()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    uvicorn.run(app, host="0.0.0.0", port=port)
