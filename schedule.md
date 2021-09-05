---
layout: default
title: Schedule
active_tab: items
---



{% for module in site.data.modules %}

<!-- Create an HTML anchor for the current module -->
{% assign anchor_created = false %}
{% capture now %}{{'now' | date: '%s'}}{% endcapture %}

{% capture module_start_date %}{{module.start_date  | date: '%s'}}{% endcapture %}

{% capture module_end_date %}{{module.end_date  | date: '%s'}}{% endcapture %}



{% if module_start_date <= now and module_end_date > now %}
<a name="now"></a>
{% endif %}

<!-- End create an HTML anchor for the current module -->


## Module {{module.module_number}} - {{module.title}} 
{% assign curr_date = module_start_date %}




<!-- Begin university calendar -->
{% for cal_item in site.data.university_calendar %}

{% capture cal_date %}{{cal_item.date | date: '%s'}}{% endcapture %}

{% if curr_date <= cal_date  and cal_date < module_end_date %}
* {{ cal_item.date | date: '%a, %b %-d, %Y' }} - {{ cal_item.title }}
{% endif %}

{% endfor %}
<!-- End university calendar -->


<!-- Assign lectures to modules based on date -->
{% for lecture in site.data.lectures %}

{% capture lecture_date %}{{lecture.date | date: '%s'}}{% endcapture %}

{% if curr_date <= lecture_date  and lecture_date < module_end_date %}
* {{ lecture.date | date: '%a, %b %-d, %Y' }} - {{ lecture.title }}
{% assign curr_date = lecture_date %}
{% endif %}

{% endfor %}

<!-- End assign lectures to modules based on date -->

{% endfor %}