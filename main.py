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



# Dictionary mapping icon names to their SVG strings
ICONS = {
    'google': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{svgs.google.brands}</svg>''',
    'microsoft': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{svgs.microsoft.brands}</svg>''',
    'sun': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-sun"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>''',
    'moon': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-moon"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>''',
    'house': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-house"><path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>''',
    'map': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-map"><path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/><path d="M15 5.764v15"/><path d="M9 3.236v15"/></svg>''',
    'calendar': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-calendar-days"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/><path d="M8 14h.01"/><path d="M12 14h.01"/><path d="M16 14h.01"/><path d="M8 18h.01"/><path d="M12 18h.01"/><path d="M16 18h.01"/></svg>''',
    'table': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-filter"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>''',
    'heart': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-heart"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>''',
    'handshake': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-handshake"><path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/><path d="m21 3 1 11h-2"/><path d="M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3"/><path d="M3 4h8"/></svg>''',
    'user_gear': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-user-round-cog"><path d="M2 21a8 8 0 0 1 10.434-7.62"/><circle cx="10" cy="8" r="5"/><circle cx="18" cy="18" r="3"/><path d="m19.5 14.3-.4.9"/><path d="m16.9 20.8-.4.9"/><path d="m21.7 19.5-.9-.4"/><path d="m15.2 16.9-.9-.4"/><path d="m21.7 16.5-.9.4"/><path d="m15.2 19.1-.9.4"/><path d="m19.5 21.7-.4-.9"/><path d="m16.9 15.2-.4-.9"/></svg>''',
    'chevron_left': '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-left"><path d="m15 18-6-6 6-6"/></svg>''',
    'menu': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-menu"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>',
    'lamp': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-lamp"><path d="M8 2h8l4 10H4L8 2Z"/><path d="M12 12v6"/><path d="M8 22v-2c0-1.1.9-2 2-2h4a2 2 0 0 1 2 2v2H8Z"/></svg>',
    'arrow_up': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-trending-up"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>',
    'search': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-search"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
    'database': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-database"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/></svg>',
    'crosshair': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-crosshair"><circle cx="12" cy="12" r="10"/><line x1="22" x2="18" y1="12" y2="12"/><line x1="6" x2="2" y1="12" y2="12"/><line x1="12" x2="12" y1="6" y2="2"/><line x1="12" x2="12" y1="22" y2="18"/></svg>',
    'store': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-store"><path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"/><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4"/><path d="M2 7h20"/><path d="M22 7v3a2 2 0 0 1-2 2a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 16 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 12 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 8 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 4 12a2 2 0 0 1-2-2V7"/></svg>',
    'expand': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-maximize-2"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" x2="14" y1="3" y2="10"/><line x1="3" x2="10" y1="21" y2="14"/></svg>',
    'compress': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-minimize-2"><polyline points="4 14 10 14 10 20"/><polyline points="20 10 14 10 14 4"/><line x1="14" x2="21" y1="10" y2="3"/><line x1="3" x2="10" y1="21" y2="14"/></svg>',
    'login': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-log-in"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" x2="3" y1="12" y2="12"/></svg>',
    'logout': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-log-out"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/></svg>',
    'register': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-user-round-plus"><path d="M2 21a8 8 0 0 1 13.292-6"/><circle cx="10" cy="8" r="5"/><path d="M19 16v6"/><path d="M22 19h-6"/></svg>',
    'font_plus': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-a-arrow-up"><path d="M3.5 13h6"/><path d="m2 16 4.5-9 4.5 9"/><path d="M18 16V7"/><path d="m14 11 4-4 4 4"/></svg>',
    'font_minus': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-a-arrow-down"><path d="M3.5 13h6"/><path d="m2 16 4.5-9 4.5 9"/><path d="M18 7v9"/><path d="m14 12 4 4 4-4"/></svg>',

    # Add other icons here...

}

def get_icon(name: str, size: float = 1.5) -> NotStr:
    """Return SVG icon wrapped in NotStr.

    Args:
        name: Name of the icon to return
        size: Size in em units (default 1.5em matches typical icon size)

    Returns:
        NotStr wrapped SVG icon

    Raises:
        KeyError: If icon name is not found
    """
    try:
        icon = ICONS[name.lower()]
        # Replace default size with specified size if different
        if size != 1.5:
            icon = icon.replace('width="1.5em"', f'width="{size}em"')
            icon = icon.replace('height="1.5em"', f'height="{size}em"')
        return NotStr(icon)
    except KeyError:
        raise KeyError(f"Icon '{name}' not found. Available icons: {', '.join(sorted(ICONS.keys()))}")

# Optional helper function for different standard sizes
def get_icon_sized(name: str, size: str = 'md') -> NotStr:
    """Get icon with predefined size.

    Args:
        name: Icon name
        size: Size name ('xs'=0.75em, 'sm'=1em, 'md'=1.5em, 'lg'=2em, 'xl'=3em)

    Returns:
        NotStr wrapped SVG icon
    """
    sizes = {
        'xs': 0.75,  # Smaller than text
        'sm': 1.0,   # Same as text
        'md': 1.5,   # Default size
        'lg': 2.0,   # Larger than text
        'xl': 3.0    # Extra large
    }
    return get_icon(name, sizes.get(size, 1.5))


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
