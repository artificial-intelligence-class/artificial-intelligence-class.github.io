---
title: CIS 521 - Artificial Intelligence - University of Pennsylvania
layout: default
img: HAL.png
img_link: https://en.wikipedia.org/wiki/HAL_9000
caption: I am putting myself to the fullest possible use, which is all I think that any conscious entity can ever hope to do. 
active_tab: main_page 
---


<!-- Display an alert about upcoming homework assignments -->
{% capture now %}{{'now' | date: '%s'}}{% endcapture %}
{% for page in site.pages %}
{% if page.release_date and page.due_date %}
{% capture release_date %}{{page.release_date | date: '%s'}}{% endcapture %}
{% capture due_date %}{{page.due_date | date: '%s'}}{% endcapture %}
{% if release_date < now and due_date >= now %}
<div class="alert alert-info">
<a href="{{page.url}}">{{ page.title }}</a> has been released.  
{% if page.deliverables %}
The assignment has multiple deliverables.
<ul>
{% for deliverable in page.deliverables %}
<li>{{ deliverable.due_date | date: "%b %-d, %Y" }} - {{deliverable.description}}.</li>
{% endfor %}
</ul>
{% else %}
It is due before {{ page.due_date | date: "%I:%M %p" }} on {{ page.due_date | date: "%A, %B %-d, %Y" }}.
{% endif %}
</div>
{% endif %}
{% endif %}
{% endfor %}
<!-- End alert for upcoming homework assignments -->


<div class="alert alert-warning">
Interested in CIS 421/521 but didn't get in?  You can <a href="https://forms.cis.upenn.edu/waitlist/index.php">add yourself to waitlist</a>. Priority will be given to graduating students who need the course for their major requirements.
</div>



Course number
: CIS 530 - Computational Linguistics 

Instructor
: [Chris Callison-Burch](http://www.cis.upenn.edu/~ccb/)

Discussion Forum
: [Piazza](https://piazza.com/upenn/fall2018/cis521)

Time and place
: Fall 2018, Tuesdays and Thursdays 12-1:30, Wu and Chen Auditorium (Levine 101)

Office hours
: TBD

Textbook
: [Artificial Intelligence: A Modern Approach (3rd edition) by Russel and Norvig](https://www.amazon.com/Artificial-Intelligence-Approach-Stuart-Russell/dp/9332543518/)

Grading
: TBD


Collaboration Policy
: Unless otherwise noted, you are not allowed to work in groups on the homework assignments. There is no project for this course.

Late Day Policy
: Each student has five free "late days".  Homeworks can be submitted at most two days late.  If you are out of late days, then you will not be able to submit your homework. One "day" is defined as anytime between 1 second and 24 hours after the homework deadline. The intent of the late day policy it to allow you to take extra time due to unforseen circumstances like illnesses or family emergencies, and for forseeable interruptions like on campus interviewing and religious holidays.  You do not need to ask permission to use your late days.  No additional late days are granted. 
