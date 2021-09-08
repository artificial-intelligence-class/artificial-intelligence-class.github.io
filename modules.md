---
layout: default
title: Modules
active_tab: recordings
---


<div class="alert alert-info">
Below, you'll find links to pre-recorded lectures. You can <a href="https://upenn.hosted.panopto.com/Panopto/Pages/Sessions/List.aspx?folderID=3ab2be61-27fe-4d23-bcfe-ad90016c91f3">watch recordings of the live lectures from this semester</a>.
</div>




<!-- Create a HTML anchor for the most recent lecture -->
{% assign anchor_created = false %}
{% capture now %}{{'now' | date: '%s'}}{% endcapture %}
{% capture this_year %}{{'now' | date: '%Y'}}{% endcapture %}

<!-- End create a HTML anchor for the most recent lecture -->




{% for module in site.data.modules %}

# Module {{ forloop.index }}: {{module.title}}

{{module.description}}


{% if module.intro_video %}  * **Intro:** Module {{ forloop.index }} [[Video]]({{module.intro_video}}) {% endif %}
{% for lesson in module.lessons %}
* **Lesson {{ forloop.index }}:** {{lesson.title}}
{%if lesson.video %}[[Video]]({{lesson.video}}){% endif %}
{% endfor %}


{% if module.slides %}
Slides: [[Slides]](slides/{{module.slides}})
{% endif %}


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

{% if module.homework %} 
Homework:

<ul>
{% for page in site.pages %}
{% capture due_year %}{{page.due_date | date: '%Y'}}{% endcapture %}

{% if page.title contains module.homework %}
<li><a href="{{page.url}}">{{ page.title }}</a> {% if this_year == due_year %}  (due {{ page.due_date | date: "%A, %B %-d, %Y" }}) {% endif %}</li>
{% endif %}
{% endfor %}
</ul>
{% endif %}



{% if module.quiz %} 
Quiz:

<ul>
{% for quiz in module.quiz %}

{% capture due_year %}{{quiz.due_date | date: '%Y'}}{% endcapture %}
<li> {{ quiz.title }}  {% if this_year == due_year %}  (due {{ quiz.due_date | date: "%A, %B %-d, %Y" }})  {% endif %}</li>
{% endfor %}
</ul>
{% endif %}




{% endfor %}