---
title: CIS 421/521 - Artificial Intelligence - University of Pennsylvania
layout: default
img: R2D2.png
active_tab: main_page 
---


<div class="alert alert-success" markdown="1">
The Fall 2019 class is full.  There are currently 150 students enrolled in the class, and another 100+  students on the waitlist. [You can sign yourself up for the waitlist](https://forms.cis.upenn.edu/waitlist/index.php) if you'd like to try to get a spot. 
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
<div class="alert alert-warning" markdown="1">
[Here is the robot checkout form.](https://docs.google.com/forms/d/e/1FAIpQLSdwSUTomNOdcsx0d1u3j57fQ9AqKiGei435-gAnbS1lfLuyhA/viewform?usp=sf_link)
</div>
-->

<div class="alert alert-info" markdown="1">
R2D2 Assignments:
* [Program robots with Python](r2d2_assignments/hw1/homework1.html)
* [A* Search](r2d2_assignments/hw2/homework2.html)
</div>



Course number
: CIS 421/521 - Artificial Intelligence 

Instructor
: [Chris Callison-Burch](https://www.cis.upenn.edu/~ccb/)

Discussion Forum
: [Piazza](http://piazza.com/upenn/fall2019/cis521)

Time and place
: Tuesdays and Thursdays from noon-1:30pm in Wu and Chen Auditorium (Levine Hall room 101)

Office hours
: TBD

Textbook
: [Artificial Intelligence: A Modern Approach (3rd edition) by Russel and Norvig](https://www.amazon.com/Artificial-Intelligence-Approach-Stuart-Russell/dp/9332543518/)

<!-- Grading
: 55% Homework Assignments
: 45% Three Midterms -->


Grading
: 55% Homework Assignments
: 15% Midterm 1
: 15% Midterm 2
: 15% Midterm 3 <br/>
There roughly one homework assignment per week, aside from weeks with exams.  Students enrolled in CIS 421 may skip one HW assignment, or they may discard their lowest scoring HW assignment.  You do not get late days back on the homework that you discard.  Students enrolled in CIS 521 must complete all HW assignments and cannot discard their lowest scoring assignment.


Collaboration Policy
: Unless otherwise noted, you are not allowed to work in groups on the homework assignments. You can discuss homework problems with others (you must explicitly list who you discussed problems with on each homework submission), but   *all code must be your own independent work.*  You are not allowed to upload your code to publicly accessible places (like public github repositories), and you are not allowed to access anyone else's code.  If you discover someone else's code online, please report it to the course staff via a private note on Piazza. 


Late Day Policy
: Each student has five free "late days".  Homeworks can be submitted at most two days late.  If you are out of late days, then you will not be able to get credit for subsequent late assignments. One "day" is defined as anytime between 1 second and 24 hours after the homework deadline. The intent of the late day policy it to allow you to take extra time due to unforseen circumstances like illnesses or family emergencies, and for forseeable interruptions like on campus interviewing and religious holidays.  You do not need to ask permission to use your late days.  No additional late days are granted. 

