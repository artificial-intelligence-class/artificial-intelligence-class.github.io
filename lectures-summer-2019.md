---
layout: default
title: Lectures
active_tab: lectures-summer-2019
---

<!-- Create a HTML anchor for the most recent lecture -->
{% assign anchor_created = false %}
{% capture now %}{{'now' | date: '%s'}}{% endcapture %}
<!-- End create a HTML anchor for the most recent lecture -->


<div class="alert alert-info">
You can <a href="https://upenn.hosted.panopto.com/Panopto/Pages/Sessions/List.aspx?folderID=8fbdc22b-8b81-4c58-b819-a9460066259e">watch recordings of the Fall 2018 lecture videos online</a>.
</div>

The lecture schedule will be updated as the term progresses. 

<table class="table table-striped">
  <thead>
    <tr>
      <th>Date</th> 
      <th>Topic</th>
      <th>Required Readings</th>
      <th>Quiz</th>
      <!-- <th>Homework</th> -->
      <!-- <th>Supplemental Videos</th> -->
    </tr>
  </thead>
  <tbody>
    {% for lecture in site.data.lectures-summer-2019 %}

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
      {% else if lecture.type and lecture.type == 'no_lecture' %}
        class="success"
      {% endif %}
    {% endif %}
    >

    <!-- End create a HTML anchor for the most recent lecture -->
      <td width="12%">{{ lecture.date | date: '%a, %b %-d, %Y' }}</td>
      <td width="30%">
         {{ title.name }}
        {% for title in lecture.titles %} 
        {% if lecture.type == nil %}
        -
        {% endif %} 
         {{ title.name }}
        <br />
        {% endfor %}

        {% if lecture.slides %}
          <a href="assets/slides/{{ lecture.slides }}">[slides]</a>
        {% endif %}


        {% if lecture.recording %}
          <a href="{{ lecture.recording }}">[video] </a>
        {% endif %}

      {% if lecture.speaker %}
          {% if lecture.speaker_url %}
            by <a href="{{ lecture.speaker_url }}">{{ lecture.speaker }}</a> 
          {% else %} 
          by {{ lecture.speaker }}
          {% endif %}
      {% endif %}

      </td>
      <td width="30%">
        {% if lecture.readings %} 
          {% for reading in lecture.readings %}
          {% if reading.url %}
              {% if reading.optional %}<b>Optional:</b> {% endif %}
              {{ reading.authors }}, <a href="{{ reading.url }}">{{ reading.title }}</a> 
            <br />
          {% else %}
              {% if reading.optional %}<b>Optional:</b> {% endif %}
             {{ reading.authors }}, {{ reading.title }} 
            <br />
          {% endif %}
          {% endfor %}
        {% endif %}
      </td>
      <td width="auto">
      {% if lecture.quiz %}
        {% for q in lecture.quiz %}
          {{ q.title }}: <a href="{{ q.url }}">{{ q.name }}</a>
            <br />
        {% endfor %}
      {% endif %}
      </td>
    </tr>

    {% if lecture.homeworks %}
      <tr
      {% if anchor_created != true and lecture_date >= now %}
        {% assign anchor_created = true %}
        id="now" 
      {% endif %}
      class="info" >
        <td>{{ lecture.date | date: '%a, %b %-d, %Y' }}</td>
        <td>
          {% for homework in lecture.homeworks %}
          {{ homework.title }}: <a href="{{ homework.url }}">{{ homework.name }}</a>
          <br/>
            {% if homework.due %}
            <td>(due by {{ homework.due | date: '%a, %b %-d, %Y' }} midnight)</td>
            {% endif %}
          {% endfor %}
        </td>
        <td></td>
      </tr>
    {% endif %}

    {% endfor %}
  </tbody>
</table>
