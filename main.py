from fasthtml.common import *
import os
from starlette.responses import PlainTextResponse  # Add this import

css_inline = r'''
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
'''

# CSS Debugging
css_debug = Style('*, *::before, *::after {box-sizing: border-box; outline:1px solid lime;}')

# View Transitions API
styles_view_transitions = '''
/* Enable view transitions globally */
html::view-transition-old(root),
html::view-transition-new(root) {
  animation: none;
  mix-blend-mode: normal;
}

/* Define the animations */
@keyframes fade-in {
  from { opacity: 0; }
}

@keyframes fade-out {
  to { opacity: 0; }
}

@keyframes slide-from-right {
  from { transform: translateX(90px); }
}

@keyframes slide-to-left {
  to { transform: translateX(-90px); }
}

/* Custom transition group */
::view-transition-group(custom) {
  animation-duration: 300ms;
}

::view-transition-old(custom) {
  animation: 90ms cubic-bezier(0.4, 0, 1, 1) both fade-out,
            300ms cubic-bezier(0.4, 0, 0.2, 1) both slide-to-left;
}

::view-transition-new(custom) {
  animation: 210ms cubic-bezier(0, 0, 0.2, 1) 90ms both fade-in,
            300ms cubic-bezier(0.4, 0, 0.2, 1) both slide-from-right;
}

/* Class for transitioning elements */
.transition-group {
  view-transition-name: custom;
}
'''
global_transitions = """
htmx.config.globalViewTransitions = true;
"""
container_toggle = '''
function toggleContainer() {
    const body = document.querySelector('body.container, body.container-fluid');
    if (body) {
        const isFluid = body.classList.contains('container-fluid');
        if (!isFluid) {
            body.classList.replace('container', 'container-fluid');
            localStorage.setItem('layout-fluid', 'true');
        } else {
            body.classList.replace('container-fluid', 'container');
            localStorage.setItem('layout-fluid', 'false');
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const body = document.querySelector('body.container, body.container-fluid');
    const isFluid = localStorage.getItem('layout-fluid') === 'true';

    if (body) {
        body.classList.remove('container', 'container-fluid');
        body.classList.add(isFluid ? 'container-fluid' : 'container');
    }
});
'''

style_resize = """
:root {
    --pico-font-family-sans-serif: Inter, system-ui, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, Helvetica, Arial, "Helvetica Neue", sans-serif, var(--pico-font-family-emoji);
    --pico-font-size: 87.5%;
    --pico-line-height: 1.25;
    --pico-form-element-spacing-vertical: 0.5rem;
    --pico-form-element-spacing-horizontal: 1.0rem;
    --pico-border-radius: 0.375rem;
    --spacing: 0;
}

@media (min-width: 576px) {
    :root {
        --pico-font-size: 87.5%;
    }
}

@media (min-width: 768px) {
    :root {
        --pico-font-size: 87.5%;
    }
}

@media (min-width: 1024px) {
    :root {
        --pico-font-size: 87.5%;
    }
}

@media (min-width: 1280px) {
    :root {
        --pico-font-size: 87.5%;
    }
}

@media (min-width: 1536px) {
    :root {
        --pico-font-size: 87.5%;
    }
}

h1, h2, h3, h4, h5, h6 {
    --pico-font-weight: 600;
}

article {
    border: 1px solid var(--pico-muted-border-color);
    /* Original doesn't have a border */
    border-radius: calc(var(--pico-border-radius) * 2);
    /* Original: var(--pico-border-radius) */
}
"""

exception_handlers={
    404: lambda req, exc: Titled("404: I don't exist!"),
    418: lambda req, exc: Titled("418: I'm a teapot!")
}

app, rt = fast_app(pico=True,
    hdrs=(
        Meta(name="view-transition", content="same-origin"),
        Style(styles_view_transitions),
        Script(global_transitions),
        Script(css_inline),
        Script(container_toggle),
        Style(style_resize)
    ),
)

# Add health check route
@rt("/health")
def get():
    # Return plain text "OK" with 200 status code
    return PlainTextResponse("OK", status_code=200)



def layout():
    return (
        Title('Layout'),
        Body(
            Style("""
            /* Base grid layout */
            me {
                min-height: 100vh;
                min-height: 100dvh;
                height: 100%;
                display: grid;
                grid-template: auto 1fr auto / auto 1fr auto;
                gap: var(--pico-spacing);
            }
            me > Nav {grid-column: 1/3;}
            me > Aside {grid-column: 1/2; padding: 0;}
            me > Main {grid-column: 2/4; padding: 0;}
            me > Footer {grid-column: 1/4; padding: 0;}

            /* Primary layout Articles only */
            me > Aside > Article,
            me > Main > Article {
                height: 100%;
                display: flex;
                flex-direction: column;
            }

            /* Primary layout Article internals */
            me > Aside > Article > Main,
            me > Main > Article > Main {
                flex: 1;
                min-height: 0;  /* Prevents overflow issues */
                overflow-y: auto;  /* Enables scrolling for overflow content */
            }

            /* Nested Articles retain normal PicoCSS behavior */
            me Article Article {
                /* Default PicoCSS article styling remains unchanged */
                display: block;  /* Reset to block for nested articles */
                height: auto;    /* Allow natural height */
            }
            """),
            Nav(
                Ul(Kbd('Event OS')),
                Ul(Li(A('Some Link', href='/#')),
                   Li(A('Someother Line', href='/#'))),
                Ul(Li(Button('Sign In', cls='outline')),
                   Li(Button("Toggle theme",
                            onclick="document.documentElement.setAttribute('data-theme', document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light')")),
                   Li(Button("Toggle Width", onclick="toggleContainer()")))
            ),
            Aside(
                Article(Header(A('My Account')),
                        Main(Ul(Li(A('Home')),
                                Hr(),
                                Li(A('Map')),
                                Li(A('Calendar')),
                                Li(A('Data Table')),
                                Hr(),
                                Li(A('Favorites')),
                                Li(A('Partnerships')),
                                Li(A('Watching')))),
                        Footer(A('settings')))
            ),
            Main(
                Article(
                    Header('this is a header'),
                    Main(P('This is actually not that big of a deal'),
                        Article(
                            Header('this is a header'),
                            Main(P('This is actually not that big of a deal')),
                            Footer('But is worth figuring out')
                        ),),
                    Footer('But is worth figuring out'))
            ),
            Footer(
                Small('EventOS LLC 2025 All Rights Reserved')
            ),
            cls='container-fluid'
        )
    )

# Home Page
@rt('/')
def get():
    return layout()



if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    uvicorn.run(app, host="0.0.0.0", port=port)
