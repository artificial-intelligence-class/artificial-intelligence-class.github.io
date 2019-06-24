---
layout: default
title: Schedule
active_tab: items
---


<div class="alert alert-info">
You can <a href="https://upenn.hosted.panopto.com/Panopto/Pages/Sessions/List.aspx?folderID=8fbdc22b-8b81-4c58-b819-a9460066259e">watch recordings of the item videos online</a>.
</div>

The schedule will be updated as the term progresses. 

{% for item in site.data.schedule %}


<div class="media">
  {% if item.thumbnail %}
  <img class="mr-3" style="width: 200px;" src="assets/img/thumbnails/{{ item.thumbnail }}">
  {% endif %}
    <div class="media-body">
    <h4 class="mt-0">{{ item.date | date: '%A, %B %-d, %Y' }}</h4>
    <h5 class="mt-0">{{ item.title }}</h5>

{% if item.type == 'video' %}
<p>{{ item.description }}
<a href="{{item.recording}}">Watch the video</a>
and 
<a href="assets/slides/{{item.slides}}">read the slides</a>

</p>
{% endif %}

{% if item.readings %}
<ul class="list-group">
<li class="list-group-item active">Readings</li>
{% for reading in item.readings %}
<li class="list-group-item">
          {% if reading.url %}
              {% if reading.optional %}<b>Optional:</b> {% endif %}
              {{ reading.authors }}, <a href="{{ reading.url }}">{{ reading.title }}</a> 
          {% else %}
              {% if reading.optional %}<b>Optional</b> {% endif %}
             {{ reading.authors }}, {{ reading.title }} 
          {% endif %}
</li>
{% endfor %}
</ul>
{% endif %}

    </div>
</div>

{% endfor %}