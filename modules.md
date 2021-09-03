---
layout: default
title: Modules
active_tab: lectures
---

<!-- Create a HTML anchor for the most recent lecture -->
{% assign anchor_created = false %}
{% capture now %}{{'now' | date: '%s'}}{% endcapture %}
<!-- End create a HTML anchor for the most recent lecture -->


{% for module in site.data.modules %}

# Module {{ forloop.index }}: {{module.title}}

{{module.description}}

{% for lesson in module.lessons %}
* **Lesson {{ forloop.index }}:** {{lesson.title}}
{%if lesson.video %}[[Video]]({{lesson.video}}){% endif %}
{%if lesson.slies %}[[Slides]]({{lesson.slides}}){% endif %}
{% endfor %}


{% if module.readings %} 
Readings:
{% for reading in module.readings %}
{% if reading.url %}
*  {% if reading.optional %}<b>Optional:</b> {% endif %} {{ reading.authors }}, <a href="{{ reading.url }}">{{ reading.title }}</a> 
{% else %}
*  {% if reading.optional %}<b>Optional</b> {% endif %} {{ reading.authors }}, {{ reading.title }} 
{% endif %}
{% endfor %}
{% endif %}


{% endfor %}