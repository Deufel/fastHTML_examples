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



@rt('/')
def get():
    """Main route that sets up the skeleton with loading sections"""
    return Div(
        Nav(Style('''
            me html {
                scroll-padding-top: calc(var(--pico-nav-element-spacing-vertical) * 3);
                scroll-behavior: smooth;
            }

            me {
                position: sticky;
                top: 0;
                left: 0;
                right: 0;
                z-index: 1000;
                /* Use Pico's spacing variables */
                padding: var(--pico-nav-element-spacing-vertical) var(--pico-nav-element-spacing-horizontal);
                /* Use Pico's transition variable */
                transition: all var(--pico-transition);
                /* Use Pico's background and border variables */
                background: color-mix(in srgb, var(--pico-background-color) 31%, transparent);
                border: var(--pico-border-width) solid color-mix(in srgb, var(--pico-background-color) 37%, transparent);
                /* Use Pico's border-radius variable */
                border-radius: var(--pico-border-radius);
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(6.3px);
                -webkit-backdrop-filter: blur(6.3px);
            }


        '''),
             # Using Pico's native nav patterns - no custom classes needed for basic structure
            Ul(Li(Img(src='static/logo.png', alt="EventOS", width="150", height="auto"))),
            Ul(
                Li(Details(
                    Summary(get_icon('menu'), 'Menu', cls="contrast"),
                    # Use role="list" for Pico's native dropdown styling
                    Ul(
                        Li(A("About", href="#about", cls="contrast secondary")),
                        Li(A("Features", href="#features", cls="contrast secondary")),
                        Li(A("Coverage", href="#coverage", cls="contrast secondary")),
                        Li(A("Pricing", href="#pricing", cls="contrast secondary")),
                        Li(Hr()),
                        # Use Pico's button styles directly
                        Li(Button(get_icon('login'),"Sign In", hx_get="/login", hx_target="body", hx_push_url="true", cls="outline")),
                        Li(Button(get_icon('register'),"Register", hx_get="/register", hx_target="body", hx_push_url="true", cls="outline contrast")),
                        Li(Hr()),
                        Li(Button(
                            Span(get_icon('sun'), cls="theme-icon light"),
                            Span(get_icon('moon'), cls="theme-icon dark"),
                            id="theme-toggle",
                            cls="outline contrast",
                            aria_label="Toggle theme"
                        )),
                        Li(Button(
                            Span(get_icon('expand'), cls="layout-icon expand"),
                            Span(get_icon('compress'), cls="layout-icon compress"),
                            id="layout-toggle",
                            cls="outline contrast",
                            aria_label="Toggle layout"
                        )),
                        role="list",
                    ),
                    dir='rtl',
                    cls="dropdown"
                ))
            ),
            cls="container"
        ),
        Main(Style('''
            me {
                /* Use Pico's spacing variables */
                padding-top: calc(var(--pico-nav-element-spacing-vertical) * 3);
            }
        '''),
            # Hero section
            Section(
                Div(Progress()),
                id="hero",
                hx_get="/sections/hero",
                hx_trigger="load",
                hx_swap="innerHTML"
            ),
            # Hero 2
            Section(
                Div(Progress()),
                id="hero",
                hx_get="/sections/temp",
                hx_trigger="load",
                hx_swap="innerHTML"
            ),
             # Hero 3
            Section(
                Div(Progress()),
                id="hero",
                hx_get="/sections/temp_2",
                hx_trigger="load",
                hx_swap="innerHTML"
            ),
            # About section
            Hgroup(Section(
                    H2('Why'),
                    Div(Progress()),
                    id="about",
                    hx_get="/sections/why",
                    hx_trigger="load",
                    hx_swap="innerHTML")),
            # Features section
            Hgroup(H2('Features'),
                Section(
                    Div(Progress()),
                    id="features",
                    hx_get="/sections/features",
                    hx_trigger="load",
                    hx_swap="innerHTML")
            ),
            # Coverage section
            Hgroup(H2('Coverage'),
                Section(
                    Div(Progress()),
                    id="coverage",
                    hx_get="/sections/coverage",
                    hx_trigger="load",
                    hx_swap="innerHTML")
            ),
            # Pricing section
            Hgroup(H2('Pricing'),
                Section(
                    Div(Progress()),
                    id="pricing",
                    hx_get="/sections/pricing",
                    hx_trigger="load",
                    hx_swap="innerHTML")
            ),
            cls="container"  # Add container class to main
        ),
        # Footer section
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
            P("© 2024 EventOS. All rights reserved.", cls="text-center"),
            cls="container"  # Add container class to footer
        )
    )

#| export

@rt("/sections/hero")
def get():
    """Hero section"""
    return Article(
        Style('''
            me {
                position: relative;
                width: 60%;
                margin: 0 auto;
                padding: 2rem;
                border-radius: var(--pico-border-radius);
                background: var(--pico-card-background-color);
                box-shadow:
                    20px 20px 60px var(--pico-card-sectionning-background-color),
                    -20px -20px 60px var(--pico-background-color);
            }

            me::before {
                content: "";
                position: absolute;
                top: -4px;    /* Increased from -2px for thicker border */
                left: -4px;
                right: -4px;
                bottom: -4px;
                background: linear-gradient(to right, #CA2B39, #0067ff);
                border-radius: calc(var(--pico-border-radius) + 4px);
                z-index: -1;
                box-shadow:
                    inset -2px -2px 6px rgba(255, 255, 255, 0.1),
                    inset 2px 2px 6px rgba(0, 0, 0, 0.1);
            }

            me .hero-tag {
                text-transform: uppercase;
                color: var(--pico-primary);
                font-weight: bold;
                letter-spacing: 0.1em;
                margin-bottom: 1rem;
            }

            me .hero-title {
                font-size: 2.5rem;
                line-height: 1.2;
                margin-bottom: 1.5rem;
            }

            me .hero-description {
                font-size: 1.1rem;
                line-height: 1.6;
                color: var(--pico-muted-color);
                margin-bottom: 2rem;
            }

            @media (max-width: 768px) {
                me {
                    width: 90%;
                }
            }
        '''),

        Main(
            # Tag line
            P("DISCOVER THE OPPORTUNITY", cls="hero-tag text-center"),

            # Main headline
            H1(
                "Everything you need to help you find meaningful event partnerships to grow your business",
                cls="hero-title text-center"
            ),

            # Description
            P(
                "Born out of necessity, we have built a one-of-a-kind tool to help businesses "
                "reach their consumers by engaging in meaningful event activations in their communities",
                cls="hero-description text-center"
            ),
            Fieldset(
                Input(name='email', type='email', placeholder='Enter your email', autocomplete='email'),
                Input(type='submit', value='Notify Me', cls='outline contrast'),
                role='group'
            )
        ),
    )

@rt("/sections/about")
def get():
    """About section"""
    return Div(
        Grid(
            Article(
                H3("Our Mission"),
                P("To make it easier for brands to connect with events"),
                cls="text-center"
            ),
            Article(
                H3("Our Vision"),
                P("Create a marketplace where brands and event hosts can effortlessly connect and build partnerships"),
                cls="text-center"
            )
        ),
    )

@rt("/sections/why")
def get():
    """About section"""
    carousel_styles = """
        me { position: relative; overflow: hidden; }
        me .quote-container { display: grid; width: 100%; }
        me blockquote {
            margin: var(--pico-typography-spacing-vertical) 0;
            padding: var(--pico-spacing);
            border-left: 0.25rem solid var(--pico-blockquote-border-color);
            opacity: 0;
            transition: opacity 0.3s ease;
            grid-area: 1 / 1;
            view-transition-name: quote;
            color: var(--pico-color);
        }
        me blockquote.active { opacity: 1; }
        me blockquote footer {
            margin-top: calc(var(--pico-typography-spacing-vertical) * 0.5);
            color: var(--pico-blockquote-footer-color);
        }
        me .controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 1rem;
        }
        me button {
            background: transparent;
            border: none;
            color: var(--pico-primary);
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0.5rem 1rem;
            transition: transform 0.2s ease;
        }
        me button:hover {
            transform: scale(1.1);
            color: var(--pico-primary-hover);
        }
        me .dots {
            display: flex;
            gap: 0.5rem;
            justify-content: center;
            margin-top: 1rem;
        }
        me .dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--pico-muted-color);
            cursor: pointer;
            border: none;
            padding: 0;
        }
        me .dot.active { background: var(--pico-primary); }
    """

    # Using Surreal's Now helper for initialization
    carousel_init = Now("""
        let current = 0;
        const quotes = any('.quote', me());
        const dots = any('.dot', me());
        let timer = null;

        // Make first quote visible immediately
        quotes[0].classList.add('active');
        dots[0].classList.add('active');

        function showQuote(idx) {
            quotes.forEach(q => q.classList.remove('active'));
            dots.forEach(d => d.classList.remove('active'));
            quotes[idx].classList.add('active');
            dots[idx].classList.add('active');
        }

        function nextQuote() {
            current = (current + 1) % quotes.length;
            showQuote(current);
        }

        function prevQuote() {
            current = (current - 1 + quotes.length) % quotes.length;
            showQuote(current);
        }

        function startTimer() {
            stopTimer();
            timer = setInterval(nextQuote, 5000);
        }

        function stopTimer() {
            if (timer) clearInterval(timer);
        }

        // Set up event handlers
        me().on('mouseenter', stopTimer);
        me().on('mouseleave', startTimer);

        me('.prev', me()).on('click', ev => {
            halt(ev);
            prevQuote();
        });

        me('.next', me()).on('click', ev => {
            halt(ev);
            nextQuote();
        });

        dots.forEach((dot, idx) => {
            dot.addEventListener('click', () => {
                current = idx;
                showQuote(current);
            });
        });

        startTimer();
    """)

    quotes = [
        ("The power of experiential marketing is that it creates emotional connections through shared moments.",
         "Ivan Menezes, former Diageo CEO"),
        ("The most valuable thing in business is a connection – real, human connection. Events create those moments where brands become more than just products; they become experiences people remember.",
         "Marc Benioff, Salesforce CEO"),
        ("In-person events remain one of our most effective channels for building brand awareness and loyalty in key markets.",
         "Albert Baladi, Beam Suntory CEO"),
        ("Live events give us the opportunity to create authentic connections with our audience. It's about creating memorable experiences that align with their lifestyle and values.",
         "Michel Doukeris, CEO of AB InBev"),
        ("Digital lets you reach millions, but events let you touch hearts. That's where lasting customer relationships are built.",
         "Richard Branson, Virgin Group"),
        ("The magic of marketing happens when you can bring your brand promise to life in a tangible way. Events are the ultimate platform for that transformation.",
         "Beth Comstock, former GE Vice Chair")
    ]

    return Div(
        H1("Why Focus on Live Events", cls="text-center"),
        P("""In today's digital-first world, live events create irreplaceable moments of authentic connection.
            They transform passive observers into active participants, building emotional bonds that resonate far
            beyond the event itself. These shared experiences become the cornerstone of lasting brand relationships.""",
          cls="text-center"),
        Div(
            Style(carousel_styles),
            Div(
                Article(*(
                    Blockquote(
                        quote,
                        Footer(Cite(f"- {author}")),
                        cls="quote"
                    ) for quote, author in quotes
                ), cls="quote-container"),
                Div(
                    Button("←", cls="prev"),
                    Button("→", cls="next"),
                    cls="controls"
                ),
                Div(*(
                    Button(cls="dot") for _ in quotes
                ), cls="dots"),
                cls="carousel"
            ),
            carousel_init,
            id="quote-carousel"
        )
    )

@rt("/sections/temp")
def get():
    """Hero section"""
    return Article(
        Style('''
            me {
                position: relative;
                width: 60%;
                margin: 0 auto;
                padding: 2rem;
                border-radius: var(--pico-border-radius);
                background: var(--pico-card-background-color);
                box-shadow:
                    20px 20px 60px var(--pico-card-sectionning-background-color),
                    -20px -20px 60px var(--pico-background-color);
            }

            me::before {
                content: "";
                position: absolute;
                top: -4px;    /* Increased from -2px for thicker border */
                left: -4px;
                right: -4px;
                bottom: -4px;
                background: linear-gradient(to right, #CA2B39, #0067ff);
                border-radius: calc(var(--pico-border-radius) + 4px);
                z-index: -1;
                box-shadow:
                    inset -2px -2px 6px rgba(255, 255, 255, 0.1),
                    inset 2px 2px 6px rgba(0, 0, 0, 0.1);
            }

            me .hero-tag {
                text-transform: uppercase;
                color: var(--pico-primary);
                font-weight: bold;
                letter-spacing: 0.1em;
                margin-bottom: 1rem;
            }

            me .hero-title {
                font-size: 2.5rem;
                line-height: 1.2;
                margin-bottom: 1.5rem;
            }

            me .hero-description {
                font-size: 1.1rem;
                line-height: 1.6;
                color: var(--pico-muted-color);
                margin-bottom: 2rem;
            }

            @media (max-width: 768px) {
                me {
                    width: 90%;
                }
            }
        '''),
        Main(
            # Tag line
            P("Find. Activate. Grow. ", cls="hero-tag text-center"),

            # Main headline
            H1(
                "Everything you need to help you find meaningful event partnerships to grow your business",
                cls="hero-title text-center"
            ),

            # Description
            P(
                "Find, Activate, and Grow! EventOS helps your company grow its brand awareness. Familiarize yourself with state-issued liquor-licensed events. Search by state to view temporary licensed events that revolve around music, food, art, culture, and other specialty themes. Add states as you open up new markets, favorite events you wish to work with, and view contact information for events you want to engage with. Your next event partnership has never been this close.",
                cls="hero-description text-center"
            ),
            Fieldset(
                Input(name='email', type='email', placeholder='Enter your email', autocomplete='email'),
                Input(type='submit', value='Notify Me', cls='outline contrast'),
                role='group'
            )
        ),
    )


@rt("/sections/temp_2")
def get():
    """Hero section"""
    return Article(
        Style('''
            me {
                position: relative;
                width: 60%;
                margin: 0 auto;
                padding: 2rem;
                border-radius: var(--pico-border-radius);
                background: var(--pico-card-background-color);
                box-shadow:
                    20px 20px 60px var(--pico-card-sectionning-background-color),
                    -20px -20px 60px var(--pico-background-color);
            }

            me::before {
                content: "";
                position: absolute;
                top: -4px;    /* Increased from -2px for thicker border */
                left: -4px;
                right: -4px;
                bottom: -4px;
                background: linear-gradient(to right, #CA2B39, #0067ff);
                border-radius: calc(var(--pico-border-radius) + 4px);
                z-index: -1;
                box-shadow:
                    inset -2px -2px 6px rgba(255, 255, 255, 0.1),
                    inset 2px 2px 6px rgba(0, 0, 0, 0.1);
            }

            me .hero-tag {
                font-size: 2.5rem;
                text-transform: uppercase;
                color: var(--pico-primary);
                font-weight: bold;
                letter-spacing: 0.1em;
                margin-bottom: 1rem;
            }

            me .hero-title {
                font-size: 3rem;
                line-height: 1.2;
                margin-bottom: 1.5rem;
            }

            me .hero-description {
                font-size: 1.1rem;
                line-height: 1.6;
                color: var(--pico-muted-color);
                margin-bottom: 2rem;
            }

            @media (max-width: 768px) {
                me {
                    width: 90%;
                }
            }
        '''),
        Main(
            # Tag line
            #P("Find. Activate. Grow. ", cls="hero-tag text-center"),

            # Main headline
            H1(
                "Find. Activate. Grow.",
                cls="hero-title text-center"
            ),

            # Description
            Div(
                P(Strong("EventOS "),"helps your company grow its brand awareness by increasing activations. Browse all officially state-licensed special events and identify partnerships opportunities that allign with your brand. Your next event partnership has never been this close.",
                cls="hero-description text-center"
            ),
            Fieldset(
                Input(name='email', type='email', placeholder='Enter your email', autocomplete='email'),
                Input(type='submit', value='Notify Me', cls='outline contrast'),
                role='group'
            )
        ),
    ),
    )

@rt("/sections/features")
def get():
    """Features section"""
    features = [
        ('search', 'Discover New Markets', 'Use our intuitive search features'),
        ('database', 'Event Database', 'Growing Database of Licensed Special Events'),
        ('crosshair', 'Strategic Deployment', 'Efficiently align your marketing efforts'),
        ('arrow_up', 'Promote Organic Growth', 'Build lasting brand equity by connecting directly with new customers'),
        ('store', 'Support Local Communities','Find market alignment for your brands, while giving back to local communities'),
        ('handshake', 'Build Lasting Partnerships', 'Develop meaningful relationships with event organizers')
    ]

    return Div(Style('me .grid{grid-template-columns: repeat(auto-fill, minmax(300px, 1fr))}'),
        Grid(*[
            Article(
                get_icon(icon),
                H3(title),
                P(desc),
                cls="text-center"
            ) for icon, title, desc in features
        ])
    )


def create_pricing(is_annual: bool = False):
    """Simple stateful pricing component"""
    price = "$20" if is_annual else "$25"
    period = "/month, billed annually" if is_annual else "/month"

    return Container(
        Article(
            H2("Simple, transparent pricing"),
            P("Choose the plan that works best for you"),

            # Simple toggle that passes state
            Group(Span('Monthly'),
                  Label(
                    Input(
                        type="checkbox",
                        role="switch",
                        checked=is_annual,
                        hx_get=f"/sections/pricing?annual={not is_annual}",
                        hx_target="#pricing-container",
                        hx_swap="innerHTML"
                    ),
                    f"Annual billing (Save 20%)"
                    ),
                  Span('Annually'),

                cls="text-center"
            ),

            Grid(
                # Free tier
                Article(
                    Header(H3("Free Tier")),
                    H2("$0", Small("/month")),
                    Ul(
                        Li("Try before you buy"),
                        Li("Create a Free account"),
                        Li("Limited Events Available")
                    ),
                    Footer(Button("Choose Plan", cls="secondary outline"))
                ),

                # Pro tier
                Article(
                    Header(H3("Pro"),
                           Group(
                                Label(
                                    Input(
                                        type="checkbox",
                                        role="switch",
                                        checked=is_annual,
                                        hx_get=f"/sections/pricing?annual={not is_annual}",
                                        hx_target="#pricing-container",
                                        hx_swap="innerHTML"
                                    ),
                                    f"Annual billing (Save 20%)"
                                ),
                                cls="text-center"
                            ),
                          ),
                    H2(price, Small(period)),
                    Ul(
                        Li("Full access to All Events"),
                        Li("Event Tracking Tools"),
                        Li("Event Search Tools")
                    ),
                    Footer(Button("Choose Plan", cls="contrast"))
                )
            ),
            id="pricing-container"
        )
    )

@rt("/sections/pricing")
def get(annual: bool = False):
    """Single route handles both initial load and toggle"""
    return create_pricing(annual)

# Using Pico CSS color variables for better theme consistency
STATUS_COLORS = {
    'live': {
        'name': 'Live',
        'fill': '#3C71F7'  # Blue
    },
    'target_2025': {
        'name': 'Target 2025',
        'fill': '#8999F9'  # Light Blue
    },
    'target_2026': {
        'name': 'Target 2026',
        'fill': '#D0D2FA'  # Lightest blue
    }
}

COLORS = [Input(type="color", value=o) for o in ('#3C71F7', '#8999F9', '#D0D2FA')]



@lru_cache(maxsize=32)
def create_us_map(state_data_key: str):
    """Creates a cached US map with integrated legend."""
    state_data = dict(eval(state_data_key))

    # Load base SVG
    base_svg = Path('static/US_Map.svg').read_text()

    # Generate state styles - now with default handling
    state_styles = []
    all_states = set([
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
        'MEE', 'DC'
    ])

    # Add styles for all states, defaulting to target_2026 if not specified
    for state in all_states:
        status = state_data.get(state, 'target_2026')  # Default to 2026
        state_code = state.lower()
        state_styles.append(
            f".{state_code} {{fill: {STATUS_COLORS[status]['fill']}}}"
        )

    # Enhanced base styles with Pico CSS variables
    base_styles = """
        .state {
            fill: var(--pico-card-sectioning-background-color);
            transition: fill 0.3s ease;  /* Smooth color transitions */
        }
        .state:hover {
            fill-opacity: 0.8;  /* Subtle hover effect */
        }
        .borders, .state {
            stroke: var(--pico-contrast-background);
            stroke-width: 1;
            stroke-linejoin: round;
        }
        .dccircle {
            display: yes;
            stroke: var(--pico-contrast-background);
            stroke-width: 1;
        }
        .separator1 {
            stroke: var(--pico-contrast-background);
            stroke-width: 1;
        }
        /* Enhanced legend styles */
        .legend-box {
            fill: var(--pico-background-color);
            stroke: var(--pico-contrast-background);
            stroke-width: 1;
            rx: 6;  /* Rounded corners matching Pico */
            opacity: 0.95;
        }
        .legend-text {
            font-family: var(--pico-font-family);
            font-size: var(--pico-font-size);
            font-weight: 500;
            fill: var(--pico-color);
        }
        .legend-sample {
            stroke: var(--pico-contrast-background);
            stroke-width: 1;
            rx: 3;
        }
    """

    # Create legend elements with improved positioning
    legend_elements = []

    # Add legend background
    legend_elements.append(
        '<rect class="legend-box" x="820" y="400" width="130" height="100"/>'
    )

    # Add legend items with enhanced spacing
    for i, (status, info) in enumerate(STATUS_COLORS.items()):
        y = 420 + (i * 30)  # Increased spacing between items
        legend_elements.append(f"""
            <rect class="legend-sample" x="830" y="{y}" width="18" height="18" fill="{info['fill']}"/>
            <text class="legend-text" x="858" y="{y + 13}">{info['name']}</text>
        """)

    # Update tooltips with enhanced information
    svg = base_svg
    for state in all_states:
        status = state_data.get(state, 'target_2026')
        tooltip_text = f"{state} - {STATUS_COLORS[status]['name']}"
        svg = svg.replace(
            f'<title>{state}</title>',
            f'<title>{tooltip_text}</title>'
        )

    # Make SVG responsive
    svg = (svg.replace('width="959"', 'width="100%"')
              .replace('height="593"', 'height="100%"')
              .replace('<svg', '<svg preserveAspectRatio="xMidYMid meet"'))

    if 'viewBox' not in svg:
        svg = svg.replace('<svg', '<svg viewBox="0 0 959 593"')

    # Insert styles and legend
    svg = svg.replace(
        '</style>',
        f'{base_styles}\n{" ".join(state_styles)}\n</style>'
    ).replace(
        '</svg>',
        f'{"".join(legend_elements)}</svg>'
    )

    return NotStr(svg)

# Route handler with improved styling
@rt('/sections/coverage/map')
def get():
    state_data = {
        'IL': 'live',
        'NY': 'target_2025',
        'TX': 'target_2025',
        'CA': 'target_2025',
        'FL': 'target_2025',
        'MA': 'target_2026',
        'CO': 'target_2026',
        'MI': 'target_2026',
        'WI': 'target_2026',
    }

    state_data_key = str(frozenset(state_data.items()))

    return Article(
        Div(create_us_map(state_data_key),
            style="width: 100%; max-width: 1200px; margin: 0 auto;"),
        Footer(Grid(*COLORS))
            )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    uvicorn.run(app, host="0.0.0.0", port=port)
