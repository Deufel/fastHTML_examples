from fasthtml.common import *
import os
from starlette.responses import PlainTextResponse  # Add this import

exception_handlers={
    404: lambda req, exc: Titled("404: I don't exist!"),
    418: lambda req, exc: Titled("418: I'm a teapot!")
}

app,rt = fast_app(pico=True,exception_handlers=exception_handlers, sess_https_only:True)

# Add health check route
@rt("/health")
def get():
    # Return plain text "OK" with 200 status code
    return PlainTextResponse("OK", status_code=200)

def create_container_demo(is_fluid: bool = False):
    return Main(
            Article(
                Header(Hgroup(
                    H1("Pico CSS Container Width Demo"),
                    Small("Statefull Component Toggle between fixed and fluid width layouts"))),
                
                Label(Input(type="checkbox", role="switch", checked=is_fluid, hx_get=f"/?fluid={not is_fluid}",
                            hx_target="#layout-container", hx_swap="outerHTML"), 'Full Width'),
                
                H3("This content area will resize based on the container type:"),
                Ul(Li("Currently using: ", Strong("Fluid Width" if is_fluid else "Fixed Width")),
                   Li(Code('Main()')," with  class: ", Kbd(".container-fluid" if is_fluid else ".container")),
                   Li("Try resizing your browser window to see the difference!")),
                     
                Footer(A('Open Pico Documents in new tab', href="https://picocss.com/docs/container", target="_blank",rel="noopener noreferrer"))
            ),
        id="layout-container",
        cls="container-fluid" if is_fluid else "container"
    )

@rt("/")
def get(fluid: bool = False):
    return create_container_demo(fluid)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    uvicorn.run(app, host="0.0.0.0", port=port)
