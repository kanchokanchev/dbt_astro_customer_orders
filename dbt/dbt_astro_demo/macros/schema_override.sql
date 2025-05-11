{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set default_schema = target.schema -%}
    
    {%- if 'staging_schema' in node.tags -%}
        {{ 'STAGING' | trim }}
    {%- elif 'analytics_schema' in node.tags -%}
        {{ 'ANALYTICS' | trim }}
    {%- elif 'presentation_schema' in node.tags -%}
        {{ 'PRESENTATION' | trim }}
    {%- else -%}
        {{ default_schema }}
    {%- endif -%}
{%- endmacro %}
