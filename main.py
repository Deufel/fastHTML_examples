from fasthtml.common import *
import os
from starlette.responses import PlainTextResponse  # Add this import

exception_handlers={
    404: lambda req, exc: Titled("404: I don't exist!"),
    418: lambda req, exc: Titled("418: I'm a teapot!")
}

# CSS Debugging
css_debug = Style('*, *::before, *::after {box-sizing: border-box; outline:1px solid lime;}')

theme_toggle = '''
function toggleTheme() {
    const html = document.documentElement;
    const isDark = html.getAttribute('data-theme') === 'dark';

    // Toggle theme
    html.setAttribute('data-theme', isDark ? 'light' : 'dark');

    // Store preference
    localStorage.setItem('theme', isDark ? 'light' : 'dark');

    // Toggle icon visibility
    const sunIcon = document.getElementById('sun-icon');
    const moonIcon = document.getElementById('moon-icon');
    if (sunIcon && moonIcon) {
        sunIcon.style.display = isDark ? 'inline-block' : 'none';
        moonIcon.style.display = isDark ? 'none' : 'inline-block';
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Check for saved theme preference or use OS preference
    let theme = localStorage.getItem('theme');
    if (!theme) {
        theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    // Set initial theme
    document.documentElement.setAttribute('data-theme', theme);

    // Set initial icon visibility
    const sunIcon = document.getElementById('sun-icon');
    const moonIcon = document.getElementById('moon-icon');
    if (sunIcon && moonIcon) {
        const isDark = theme === 'dark';
        sunIcon.style.display = isDark ? 'none' : 'inline-block';
        moonIcon.style.display = isDark ? 'inline-block' : 'none';
    }

    // Listen for OS theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (!localStorage.getItem('theme')) {
            const newTheme = e.matches ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            if (sunIcon && moonIcon) {
                sunIcon.style.display = e.matches ? 'none' : 'inline-block';
                moonIcon.style.display = e.matches ? 'inline-block' : 'none';
            }
        }
    });
});
'''

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

        // Update icon visibility
        const expandIcon = document.getElementById('expand-icon');
        const compressIcon = document.getElementById('compress-icon');
        if (expandIcon && compressIcon) {
            expandIcon.style.display = !isFluid ? 'none' : 'inline-block';
            compressIcon.style.display = !isFluid ? 'inline-block' : 'none';
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

        // Set initial icon visibility
        const expandIcon = document.getElementById('expand-icon');
        const compressIcon = document.getElementById('compress-icon');
        if (expandIcon && compressIcon) {
            expandIcon.style.display = isFluid ? 'inline-block' : 'none';
            compressIcon.style.display = isFluid ? 'none' : 'inline-block';
        }
    }
});
'''

font_toggle = '''
function toggleFontSize() {
    const root = document.documentElement;
    const currentSize = getComputedStyle(root).getPropertyValue('--pico-font-size').trim();
    const isLarge = currentSize === '100%';

    // Toggle between 87.5% and 100%
    root.style.setProperty('--pico-font-size', isLarge ? '87.5%' : '100%');

    // Store preference
    localStorage.setItem('font-size-large', (!isLarge).toString());

    // Toggle icon visibility
    const plusIcon = document.getElementById('font-plus-icon');
    const minusIcon = document.getElementById('font-minus-icon');
    if (plusIcon && minusIcon) {
        plusIcon.style.display = isLarge ? 'inline-block' : 'none';
        minusIcon.style.display = isLarge ? 'none' : 'inline-block';
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const root = document.documentElement;
    const isLarge = localStorage.getItem('font-size-large') === 'true';

    // Set initial size from storage or default to large (100%)
    root.style.setProperty('--pico-font-size', isLarge ? '100%' : '87.5%');

    // Set initial icon visibility
    const plusIcon = document.getElementById('font-plus-icon');
    const minusIcon = document.getElementById('font-minus-icon');
    if (plusIcon && minusIcon) {
        plusIcon.style.display = isLarge ? 'none' : 'inline-block';
        minusIcon.style.display = isLarge ? 'inline-block' : 'none';
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
    border-radius: calc(var(--pico-border-radius) * 2);
}


.vr {
  width: 1px;
  height: 60%;
  margin: auto var(--pico-typography-spacing-vertical);
  border: 0;
  border-left: 1px solid var(--pico-contrast);
  display: inline-block;
  vertical-align: middle;
  align-self: stretch;
  color: inherit;
}

/* Added utility classes */

.text-center {text-align: center !important;}
.spacer {flex-grow: 1;height: 100%; display: flex; flex-direction: column;}

"""

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

exception_handlers={
    404: lambda req, exc: Titled("404: I don't exist!"),
    418: lambda req, exc: Titled("418: I'm Lost!")
}

app, rt = fast_app(pico=True,
    hdrs=(
        Meta(name="view-transition", content="same-origin"),
        Meta(name="viewport", content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"),
        Style(styles_view_transitions),
        Script(global_transitions),
        Script(css_inline),
        Script(container_toggle),
        Script(font_toggle),
        Script(theme_toggle),
        Style(style_resize),

        #Style(css_debug),
    ),
)

# Add health check route
@rt("/health")
def get():
    # Return plain text "OK" with 200 status code
    return PlainTextResponse("OK", status_code=200)

@rt("/test")
def get():
    return (
        Title("View Transitions Demo"),
        H1('This is a test to see if the flashing issue is gone'),
        Button("Toggle theme", onclick="document.documentElement.setAttribute('data-theme', document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light')"),
        Container(
            Div(
                Div(
                    H1("Initial Content"),
                    P("Click the button to see the transition effect!"),
                    Button(
                        "Show New Content",
                        hx_get="/test2",
                        hx_target="#main-content",
                        hx_swap="outerHTML"  # No need for transition:true now
                    ),
                    cls="content-box"
                ),
                id="main-content",
                cls="transition-group"
            )
        )
    )

@rt("/test2")
def get():
    return Div(
        Div(
            H1("New Content"),
            P("The content smoothly transitioned into view!"),
            Article('Now we have some more stuff in this swappp how does it work?'),
            Button(
                "Go Back",
                hx_get="/test",
                hx_target="#main-content",
                hx_swap="outerHTML"
            ),
            cls="content-box"
        ),
        id="main-content",
        cls="transition-group"
    )

def layout_dashboard():
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
            me > Nav {grid-column: 1/4; padding: 0}
            me > Aside {grid-column: 1/2; padding 0;
            Ul{padding:0; margin:0;}
            }
            me > Main {grid-column: 2/4; padding: 0;}
            me > Footer {grid-column: 1/4; padding: 0}

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
                overflow-y: auto;  /* Enables scrolling for overflow content SHould I Have this? */
            }

            /* Nested Articles retain normal PicoCSS behavior */
            me Article Article {
                /* Default PicoCSS article styling remains unchanged */
                display: block;  /* Reset to block for nested articles */
                height: auto;    /* Allow natural height */
            }
            """),
            Nav(
                Ul(Li(Img(src='static/logo.png', alt="EventOS", width="150", height="auto"))),
                Ul(Li(Button('Sign In')),
                   Li(Button('Register')),
                   Span(cls="vr"),
                   Li(Button(Div(get_icon('sun', 1.2), id='sun-icon', style='display: none'),
                             Div(get_icon('moon', 1.2), id='moon-icon', style='display: inline-block'),
                             id="theme-toggle-btn", onclick="toggleTheme()", cls="outline", title="Toggle theme",
                             **{'aria-label': "Toggle dark mode"})),

                   Li(Button(Div(get_icon('expand'), id='expand-icon', style='display: none'),
                             Div(get_icon('compress'), id='compress-icon', style='display: inline-block'),
                             id="container-toggle-btn",onclick="toggleContainer()",cls="outline")),

                   Li(Button(Div(get_icon('font_plus'), id='font-plus-icon', style='display: inline-block'),
                             Div(get_icon('font_minus'), id='font-minus-icon', style='display: none'),
                             id="font-toggle-btn",onclick="toggleFontSize()",cls="outline")))
            ),
            Aside(
                Article(Header(Kbd('Event OS')),
                        Main(Ul(Li(A('Home')),
                                Hr(),
                                Li(A('About', href="/#about")),
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
                    Header('Dashboard'),
                    Main(Container(
                        calendar_component(), draggable=True
                    )),
                    Footer('Footer'))
            ),
            Footer(
                Article(Small('EventOS LLC 2025 All Rights Reserved'))
            ),
            cls='container-fluid'
        )
    )

# Home Page
@rt('/dashboard')
def get():
    return layout_dashboard()


def layout_landing():
    return (
        Title('EventOS'),
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
            me > Nav {grid-column: 1/4; padding: 0}
            me > Main {grid-column: 1/4; padding: 0;}
            me > Footer {grid-column: 1/4; padding: 0}

            /* Primary layout Articles only */
            me > Aside > Article,
            me > Main > Article {
                height: 100%;
                display: flex;
                flex-direction: column;
            }
            """),
            Nav(
                Ul(Li(Img(src='static/logo.png', alt="EventOS", width="150", height="auto"))),
                Ul(Li(Button('Sign In')),
                   Li(Button('Register')),
                   Span(cls="vr"),
                   Li(Button(Div(get_icon('sun'), id='sun-icon', style='display: none'),
                             Div(get_icon('moon'), id='moon-icon', style='display: inline-block'),
                             id="theme-toggle-btn", onclick="toggleTheme()", cls="outline", title="Toggle theme",
                             **{'aria-label': "Toggle dark mode"})),

                   Li(Button(Div(get_icon('expand'), id='expand-icon', style='display: none'),
                             Div(get_icon('compress'), id='compress-icon', style='display: inline-block'),
                             id="container-toggle-btn",onclick="toggleContainer()",cls="outline")),

                   Li(Button(Div(get_icon('font_plus'), id='font-plus-icon', style='display: inline-block'),
                             Div(get_icon('font_minus'), id='font-minus-icon', style='display: none'),
                             id="font-toggle-btn",onclick="toggleFontSize()",cls="outline")))
            ),
            Main(Article(
                        # Hero section
                        Section(
                            Div(Progress()),
                            id="hero",
                            hx_get="/sections/hero",
                            hx_trigger="load",
                            hx_swap="innerHTML"
                        ),
                Hr(),
                           # Pricing section
                        Section(H1('Pricing',id="pricing", cls='text-center'),
                            Section(
                                Div(Progress()),
                                hx_get="/sections/pricing",
                                hx_trigger="load",
                                hx_swap="innerHTML")
                        ),
                Hr(),
                            # Testing for View Transitions API
                        Section(H1('Pricing',id="pricing", cls='text-center'),
                            Section(
                                Div(Progress()),
                                hx_get="/sections/test",
                                hx_trigger="load",
                                hx_swap="innerHTML")
                        ),
                    )
            ),
            Footer(
                Grid(
                    Div(
                        H4("Event OS"),
                        Nav(
                            Ul(
                                Li(A("About", href="#")),
                                Li(A("Careers", href="#")),
                                Li(A("Contact", href="#"))
                            )
                        )
                    ),
                    Div(
                        H4("Resources"),
                        Nav(
                            Ul(
                                Li(A("Documentation", href="#")),
                                Li(A("Blog", href="#")),
                                Li(A("Support", href="#"))
                            )
                        )
                    ),
                    Div(
                        H4("Legal"),
                        Nav(
                            Ul(
                                Li(A("Privacy", href="#")),
                                Li(A("Terms", href="#"))
                            )
                        )
                    )
                ),
                Hr(),
                P("© 2024 EventOS. All rights reserved.", cls="text-center")
            ),
            cls='container-fluid'
        )
    )


# Home Page
@rt('/')
def get():
    return layout_landing()


@rt("/sections/hero")
def get():
    """Hero section"""
    return Article(
        Style('''
            me {
                position: relative;
                max-width: 800px;
                width: clamp(70%, 800px, 90%);
                margin: 0 auto;
                padding: 2rem;
                border-radius: var(--pico-border-radius);
                background: var(--pico-card-background-color);
                box-shadow:
                    20px 20px 60px var(--pico-card-sectionning-background-color),
                    -20px -20px 60px var(--pico-background-color);
            }

            /* Hero content layout */
            me .hero-description {
                max-width: 66%;
                margin: 2rem auto;
                text-wrap: balance;
                text-align: center;
                line-height: 1.6;
            }

            /* Email group styling */
            me .email-group {
                display: grid;
                grid-template-columns: 1fr;
                gap: 0.5rem;
                max-width: 400px;
                margin: 0 auto;
            }

            me .input-wrapper {
                display: flex;
                gap: 0.5rem;
            }

            me .input-wrapper input[type="email"],
            me .input-wrapper input[type="submit"] {
                flex: 1;
                min-width: 0;
            }

            me .email-group small {
                text-align: left;
                margin-top: 0.25rem;
            }

            @media (max-width: 768px) {
                me {
                    width: 90%;
                    padding: 1.5rem;
                }

                me .hero-description {
                    max-width: 90%;
                }

                me .input-wrapper {
                    flex-direction: column;
                }
            }
        '''),
        Main(
            P("EVENT OS", cls="hero-tag text-center"),
            H1("Find. Activate. Grow.", cls="hero-title text-center"),
            P('''EventOS helps your company grow its brand awareness by increasing activations.
                 Browse all officially state-licensed special events and identify partnerships opportunities that align with your brand.
                 Your next event partnership has never been this close.''',
                cls="hero-description"),

            Form(
                    Label('email',
                          Input(name='email', type='email', placeholder='Sign Up for a Launch Notification ',
                            autocomplete='email', required=True, aria_describedby='email-validation'),
                          Small(id='email-validation')),
                          Button('Notify Me', type='submit', cls='outline contrast'),
                         ),

        ),
        Script('''
        document.querySelector('input[type="email"]').addEventListener('input', function(e) {
            const input = e.target;
            const message = document.querySelector('#email-validation');

            if (input.validity.valueMissing) {
                input.setAttribute('aria-invalid', 'true');
                message.textContent = 'Please enter your email address';
            } else if (input.validity.typeMismatch) {
                input.setAttribute('aria-invalid', 'true');
                message.textContent = 'Please enter a valid email address';
            } else {
                input.setAttribute('aria-invalid', 'false');
                message.textContent = 'Looks good!';
            }
        });
        ''')
    )

def create_pricing():
    """Simple pricing component with both monthly and annual prices"""
    return Div(Style('''
    /* Container for max-width */
    me {
        max-width: 1024px;
        margin: 0 auto;
    }

    /* Grid container */
    me > Grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: var(--pico-grid-row-gap);
    }

    /* Card layout */
    me Article {
        display: flex;
        flex-direction: column;
        height: 100%;
    }

    /* Push footer to bottom */
    me Article > ul {
        margin-top: auto;
        margin-bottom: var(--pico-block-spacing-vertical);
    }

    me Article > footer {
        margin-top: auto;
    }

    /* Price styling */
    me .price-block {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    me .annual-price {
        color: var(--pico-primary);
        font-size: var(--pico-font-size);
    }
    '''),
            Hgroup(
                   H3("Simple, Transparent Pricing"),
                    P("Choose the plan that works best for you")
                  ),
            Grid(
                # Free tier
                Article(
                    Header(H3("7 Day Free Trial")),
                    H2("$0"),
                    Ul(
                        Li("No Credit Card Required on Sign Up"),
                        Li("Limited Access to Event Database"),
                        Li("Full Access to Premium Features"),
                        Li('Event Tracking and Note Taking Tools'),
                        Li('Opportunity Summary Report Tracking')
                    ),
                    Footer(Button("Start Trial", cls="outline secondary", type='submit'))
                ),

                # Pro tier
                Article(
                    Header(H3("Pro")),
                    Grid(H2("$25", Small("/month")),
                         H2("$240", Small("/year"), cls='annual-price')),
                    Ul(
                        Li("Full Access to All Events"),
                        Li("Favorite Potential Event"),
                        Li("Track Event Partnerships"),
                        Li("Event CMS Tools Available"),
                        Li("Event Activation Summaries")
                    ),
                    Footer(Button("Register", cls="outline", type='submit'))
                )
            ),
            id="pricing-container"
            )

@rt("/sections/pricing")
def get():
    """Single route handles initial load"""
    return create_pricing()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    uvicorn.run(app, host="0.0.0.0", port=port)
