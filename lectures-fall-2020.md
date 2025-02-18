---
layout: default
title: Lectures
active_tab: lectures
---

<!-- Create a HTML anchor for the most recent lecture -->
{% assign anchor_created = false %}
{% capture now %}{{'now' | date: '%s'}}{% endcapture %}
<!-- End create a HTML anchor for the most recent lecture -->


The lecture schedule will be updated as the term progresses. 

<table class="table table-striped">
  <thead>
    <tr>
      <th>Date</th> 
      <th>Topic</th>
      <th>Required Readings</th>
      <th>Supplemental Videos</th>
    </tr>
  </thead>
  <tbody>
    {% for lecture in site.data.lectures-fall-2020 %}

    <!-- Create a HTML anchor for the most recent lecture -->
    {% capture lecture_date %}{{lecture.date | date: '%s'}}{% endcapture %}
    {% assign lecture_date = lecture_date | plus: 0 %}
    {% assign now = now | minus: 14400 %}

    <tr
    {% if anchor_created != true and lecture_date >= now %}
      {% assign anchor_created = true %}
      id="now" 
    {% endif %}
    {% if lecture.type %}
      {% if lecture.type and lecture.type == 'exam' %}
        class="info" 
      {% else if lecture.type and lecture.type == 'deadline' %}
        class="warning"
      {% else if lecture.type and lecture.type == 'homework' %}
        class="primary"
      {% else if lecture.type and lecture.type == 'no_lecture' %}
        class="success"
      {% endif %}
    {% endif %}
    >
    <!-- End create a HTML anchor for the most recent lecture -->
      <td width="14%">{{ lecture.date | date: '%a, %b %-d, %Y' }}</td>
      <td width="30%">
         {{ lecture.title }} 

        {% if lecture.parts %}
         <ul>
        {% for part in lecture.parts %}
          <li> {{part.title}} 
          <a href="assets/slides/{{part.slides }}">[slides]</a> </li>
        {% endfor %}
         </ul>
		{% else %}
         {% if lecture.slides %}
         <a href="assets/slides/{{lecture.slides }}">[slides]</a> 
         {% endif %}
        {% endif %}

        {% if lecture.recording %}
          <a href="{{lecture.recording }}">[video]</a> 
          {% endif %}


	    {% if lecture.speaker %}
          {% if lecture.speaker_url %}
            by <a href="{{ lecture.speaker_url }}">{{ lecture.speaker }}</a> 
          {% else %} 
          by {{ lecture.speaker }}
          {% endif %}
	    {% endif %}

      </td>
      <td>
        {% if lecture.readings %} 
          {% for reading in lecture.readings %}
          {% if reading.url %}
              {% if reading.optional %}<b>Optional:</b> {% endif %}
              {{ reading.authors }}, <a href="{{ reading.url }}">{{ reading.title }}</a> 
            <br />
          {% else %}
              {% if reading.optional %}<b>Optional</b> {% endif %}
             {{ reading.authors }}, {{ reading.title }} 
            <br />
          {% endif %}
          {% endfor %}
        {% endif %}
      </td>
       <td>
        {% if lecture.videos %} 
          {% for video in lecture.videos %}
          {% if video.authors %} {{ video.authors }}, {% endif %}
          <a href="{{ video.url }}">{{ video.title }}</a> 
          {% if video.length %} ({{ video.length }}) {% endif %}
            <br />
          {% endfor %}
        {% endif %}
      </td>
    </tr>
    {% endfor %}
    
  </tbody>
</table>

