---
layout: default
title: Schedule
active_tab: items
term_start: 2022-08-30
term_end: 2022-12-22
lecture_days: Tuesdays and Thursdays
---




<div class="alert alert-info">
You can <a href="https://upenn.hosted.panopto.com/Panopto/Pages/Sessions/List.aspx?folderID=82b51ccf-a22c-44fb-9582-ad99000835ae">watch recordings of the live lectures</a>, or you can watch <a href="modules.html">pre-recorded lectures for each module</a>.
</div>



<table class="table table-striped" >
  <thead>
    <tr>
      <th>Date</th> 
      <th>Topic</th>
    </tr>
  </thead>
  <tbody>

<!-- Walk through the days in the semester -->
<!-- Capture the current day -->
{% capture start_date %}{{page.term_start  | date: '%s'}}{% endcapture %}
{% capture end_date %}{{page.term_end  |  date: "%Y-%m-%d" }}{% endcapture %}
{% for i in (1..365) %}

{% assign seconds = {i} | times: 24 | times: 60 | times: 60 %}
{% capture curr_date %}{{ start_date | date: "%s" | plus: seconds | date: "%Y-%m-%d" }}{% endcapture %}

{% capture day_of_week %}{{ curr_date | date: "%A" }}{% endcapture %}

{% if curr_date > end_date %}
 {% break %}
{% endif %}
<!-- End of Capture the current day -->

<!-- Check to see if today is a lecture day -->
{% assign is_lecture_day = false %}
{% if page.lecture_days contains day_of_week %} 
{% assign is_lecture_day = true %}
{% endif %}
<!-- End check to see if today is a lecture day -->

<!-- Check for university calendar events -->
{% for ucal in site.data.university_calendar %}

{% capture ucal_date %}{{ucal.date | date: "%Y-%m-%d"}}{% endcapture %}
{% if ucal_date == curr_date %}
<!-- Display university calendar item -->
<tr><td>{{ ucal.date | date: '%a, %b %-d, %Y' }} </td><td>{{ ucal.title | markdownify }}
<!-- End display university calendar -->
<!-- Override lecture days for university vacation days -->
{% if ucal.type == 'no_lecture' %} (No lecture)
{% assign is_lecture_day = false %}
{% endif %}
</td></tr>
<!-- End override lecture days  -->

{% endif %}
{% endfor %}
<!-- End check for university calendar events -->


<!-- Check for module starts -->
{% for module in site.data.modules %}
{% capture module_start_date %}{{ module.start_date | date: "%Y-%m-%d"}}{% endcapture %}
{% if module_start_date == curr_date %}
<!-- Display module info -->
<tr><td>{{ module.start_date | date: '%a, %b %-d, %Y' }}</td><td>Start of Module {{module.module_number}} - {{module.title}}</td></tr>
<!-- End display module  -->
{% capture slides %}{{module.slides}}{% endcapture %}
{% endif %}


<!-- Check for quizzes -->
{% for quiz in module.quiz %}
{% capture quiz_due_date %}{{ quiz.due_date | date: "%Y-%m-%d"}}{% endcapture %}
{% if quiz_due_date == curr_date %}
<tr><td class="alert alert-info">{{ quiz.due_date | date: '%a, %b %-d, %Y' }}</td><td class="alert alert-info">
{% if quiz.url %}
<a href="{{quiz.url}}">{{quiz.title}}</a> is due.
{% else %}
{{quiz.title}} is due.
{% endif %}
{% if module.readings %}
The quiz covers: 
<ul>
{% for reading in module.readings %}
{% if reading.optional %}
{% else %}
<li>{{reading.title}}</li>
{% endif %}
{% endfor %}
</ul>
{% endif %}
</td></tr>
{% endif %}
{% endfor %}
<!-- End check for quizzes -->
{% endfor %}
<!-- End check for module starts -->



<!-- Check for exams -->
{% for exam in site.data.exams %}
{% capture exam_due_date %}{{ exam.due_date | date: "%Y-%m-%d"}}{% endcapture %}
{% if exam_due_date == curr_date %}
<tr><td class="alert alert-danger">{{ exam.due_date | date: '%a, %b %-d, %Y' }}</td><td class="alert alert-danger">
{{exam.title}} 

{% if exam.type == "in-person" %}
- in person at {{ exam.due_date | date: '%H:%M%p' }}
{% endif %}


{% if exam.type == "online" %}
- online.  Due by {{ exam.due_date | date: '%a, %b %-d, %Y %H:%M%p' }}
{% endif %}
{% if exam.url %}
<a href="{{quiz.url}}">[link]</a> 
{% endif %}
</td></tr>
{% endif %}
{% endfor %}
<!-- End check for exams -->


<!-- Check for homework due dates -->
{% for page in site.pages %}
{% if page.active_tab == "homework" %}

{% capture hw_due_date %}{{ page.due_date | date: "%Y-%m-%d"}}{% endcapture %}

{% if hw_due_date == curr_date %}
<tr><td class="alert alert-success">{{ hw_due_date | date: '%a, %b %-d, %Y' }}</td><td class="alert alert-success"><span markdown="1">[{{page.title}}]({{page.url}}) is due</span></td></tr>
{% endif %}

{% endif %}
{% endfor %}
<!-- Check for homework due dates -->






<!-- Display lecture info  -->
{% if is_lecture_day == true %}
{% assign displyed_lecture_info = false %}
{% for lecture in site.data.lectures %}
{% capture lecture_date %}{{lecture.date | date: "%Y-%m-%d"}}{% endcapture %}

{% if lecture_date == curr_date %}
<tr><td>{{ lecture_date | date: '%a, %b %-d, %Y' }}</td><td><span markdown="1">{{lecture.title}} [[recording]]({{lecture.recording}}) [[slides]](slides/{{slides}})</span></td></tr>
{% assign displyed_lecture_info = true %}
{% endif %}
{% endfor %}


<!-- Placeholder if no lecture exists in the YAML -->
{% if displyed_lecture_info == false %}
<tr><td>{{ curr_date | date: '%a, %b %-d, %Y' }} </td><td><span markdown="1">Lecture  [[slides]](slides/{{slides}})</span></td></tr>
<!-- End no lecture placeholder -->
{% endif %}

{% endif %}
<!-- End display lecture info -->



<!-- Display recitations / recorded group office hours -->
{% for recitation in site.data.recitations %}
{% capture recitation_date %}{{recitation.date | date: "%Y-%m-%d"}}{% endcapture %}

{% if recitation_date == curr_date %}
<tr><td>{{ recitation_date | date: '%a, %b %-d, %Y' }}</td><td><span markdown="1">{{recitation.title}} [[recording]]({{recitation.recording}}) 
{% if recitation.slides %}
[[slides]](slides/{{slides}})
{% endif %}
</span></td></tr>
{% endif %}
{% endfor %}
<!-- End display recitations / recorded group office hours -->

{% endfor %}
<!-- End of walk through the days in the semester -->

  </tbody>
</table>
