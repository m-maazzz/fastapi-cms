from jinja2 import Environment, FileSystemLoader
from pathlib import Path

templates_path = Path(__file__).parent.parent / "templates"
jinja_env = Environment(loader=FileSystemLoader(templates_path))

def render_template(template_name: str, context: dict) -> str:
    template = jinja_env.get_template(template_name)
    return template.render(context)
