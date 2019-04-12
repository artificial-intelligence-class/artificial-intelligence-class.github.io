---
title: CIS 521 - Artificial Intelligence - University of Pennsylvania
layout: default
img: HAL.png
img_link: https://en.wikipedia.org/wiki/HAL_9000
caption: I am putting myself to the fullest possible use, which is all I think that any conscious entity can ever hope to do. 
active_tab: main_page 
---
 
<div class="alert alert-success">
CIS 421/521 will be offered during the Summer 2 Session (July 5-August 9).  The class will meet in 3401 Walnut room 401B on Mondays, Wednesdays and Fridays from 2:30pm-5pm (not noon-2:30pm like it said during Advanced Registration). 
</div>


<div class="alert alert-success" markdown="1">
Interestred in joining the class in the Fall?  To get a permit, [you can sign yourself up for the waitlist](https://forms.cis.upenn.edu/waitlist/index.php) now. You do **not** need to contact the instructor to request permission to register.  
</div>



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
It is due before {{ page.due_date | date: "%I:%M%p" }} on {{ page.due_date | date: "%A, %B %-d, %Y" }}.
{% endif %}
</div>
{% endif %}
{% endif %}
{% endfor %}
<!-- End alert for upcoming homework assignments -->

<!-- 
<div class="alert alert-info">
The first midterm will be in-class on Tuesday October 2.  If you'd like to do a practice exam, here's a <a href="assets/practice_exams/midterm1-practice.pdf">sample of a previous year's midterm</a>. You can take a look at <a href="assets/practice_exams/midterm1-practice+ANSWERS.pdf">the sample solutions</a> after you've done it.
</div>
 -->

Course number
: CIS 421/521 - Artificial Intelligence 

Instructor
: [Chris Callison-Burch](http://www.cis.upenn.edu/~ccb/)

Discussion Forum
: [Piazza](https://piazza.com/upenn/fall2018/cis521)

Time and place
: Summer 2 Session 2019 (from July 5th through August 9th). Mondays, Wednesdays and Fridays from 2:30pm-5pm in 3401 Walnut room 401B.

Office hours
: TBD

Textbook
: [Artificial Intelligence: A Modern Approach (3rd edition) by Russel and Norvig](https://www.amazon.com/Artificial-Intelligence-Approach-Stuart-Russell/dp/9332543518/)

Grading
: 55% Homework Assignments, 15% Midterm 1, 15% Midterm 2, 15% Midterm 3.  There roughly one homework assignment per week, aside from weeks with exams.  Students enrolled in CIS 421 may skip one HW assignment, or they may discard their lowest scoring HW assignment.  You do not get late days back on the homework that you discard.  Students enrolled in CIS 521 must complete all HW assignments and cannot discard their lowest scoring assignment.

Collaboration Policy
: Unless otherwise noted, you are not allowed to work in groups on the homework assignments. You can discuss homework problems with others (you must explicitly list who you discussed problems with on each homework submission), but   *all code must be your own independent work.*  You are not allowed to upload your code to publicly accessible places (like public github repositories), and you are not allowed to access anyone else's code.  If you discover someone else's code online, please report it to the course staff via a private note on Piazza. 


Late Day Policy
: Each student has five free "late days".  Homeworks can be submitted at most two days late.  If you are out of late days, then you will not be able to get credit for subsequent late assignments. One "day" is defined as anytime between 1 second and 24 hours after the homework deadline. The intent of the late day policy it to allow you to take extra time due to unforseen circumstances like illnesses or family emergencies, and for forseeable interruptions like on campus interviewing and religious holidays.  You do not need to ask permission to use your late days.  No additional late days are granted. 
