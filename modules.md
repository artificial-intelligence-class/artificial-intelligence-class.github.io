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

# {{module.title}}

{{module.description}}

## Learning Objectives
<ul>
{% for objective in module.learning_objectives %}
<li>{{objective}}</li>
{% endfor %}
</ul>

{% for lesson in module.lessons %}

## {{lesson.title}}
<ul>
{% for topic in lesson.topics %}
<li>{{topic}}</li>
{% endfor %}
</ul>

{% endfor %}


{% endfor %}