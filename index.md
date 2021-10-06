---
title: CIS 421/521 - Artificial Intelligence - University of Pennsylvania
layout: default
img: R2D2.png
active_tab: main_page 
---

<!--
<div class="alert alert-danger" markdown="1">
**Waitlist update**: I added a second session with addition 200 spaces to the course.  That session meets Mondays and Wednesdays at 8:30am-10am in Heilmeier auditorium.  You can get a permit by signing up on [CIS Waitlist System](https://forms.cis.upenn.edu/waitlist/index.php) for CIS421/521-402.

For  questions about the waitlist or registration, please contact Lee Dukes - ldukes@seas.upenn.edu.
</div>
-->

<!--
	If you have a question about the waitlist system you can email Lee Dukes ldukes@seas.upenn.edu.  
In order to be considered for a permit for the course, you must complete the first assignment by its due date.



To register for CIS 421/521 you should sign yourself up for the [CIS Waitlist System](https://forms.cis.upenn.edu/waitlist/index.php) when it opens on April 30th.  Registration isn't available during advance registration, and you don't need to request permission of the instructor.

After you've added yourself to the waitlist, you'll get assigned a category based on your degree and how many years you have left at Penn.  

</div>
-->


<!-- Display an alert about upcoming quizzes -->
{% capture now %}{{'now' | date: '%s'}}{% endcapture %}
{% for module in site.data.modules %}
{% if module.quiz %}
{% for quiz in module.quiz %}
{% capture release_date %}{{module.start_date | date: '%s'}}{% endcapture %}
{% capture due_date %}{{quiz.due_date | date: '%s'}}{% endcapture %}
{% if release_date < now and due_date >= now %}
<div class="alert alert-info">
<a href="{{quiz.url}}">{{ quiz.title }}</a> has been released. It is due before {{ quiz.due_date | date: "%I:%M%p" }} on {{ quiz.due_date | date: "%A, %B %-d, %Y" }}.
</div>
{% endif %}
{% endfor %}
{% endif %}
{% endfor %}
<!-- End alert for upcoming quizzes -->

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


<div class="alert alert-info" markdown="1">
R2D2 ***Extra Credit*** Assignments (late submission not allowed):
* [Robot Exercise 1: Using Python to Control R2D2](r2d2_assignments/hw1/homework1.html)
* [Robot Exercise 2: Robot Navigation](r2d2_assignments/hw2/homework2.html)
* [Robot Exercise 3: Flag Capture Game using a Minimax Algorithm](r2d2_assignments/hw3/homework3.html)
* [Robot Exercise 4: Commanding Robots with Natural Language](r2d2_assignments/hw4/homework4.html)

Extra Credit Bounty Items:
* ~~Get the Python API that we developed working on Windows~~ (solved by Hanbang with Raspberry Pi)
* Find a way to communicate the robot's gyroscopic sensor info back to Python
* Develop a Python collision detection protocol 
</div>

-->



Course number
: CIS 421/521 - Artificial Intelligence

Prerequeisites
: CIS 121 (for undergraduates)
: CIT 594 (for MCIT students)
: A data structure and algorithms course, plus substantial programming experience (for everyone)

Instructor
: [Chris Callison-Burch](https://www.cis.upenn.edu/~ccb/)

Discussion Forum
: [Piazza](http://piazza.com/upenn/fall2021/cis521)

Time and place
: In Fall 2021, the course will be in-person and broadcast live via Zoom. You are not obligated to attend in person.  Everyone is welcome to watch the videos from home.
: All lecture materials will be recorded and uploaded for students wishing to participate remotely.  We also have [pre-recorded lectures available for review](modules.html).
: The first day of class is Tuesday, August 31, 2021.
: The first day of office hours will be Tuesday, September 7, 2021.
: The final day of class is Thursday, December 9, 2020.
: There are several sections of the class:
* The Monday/Wednesday section meets from 8:30am-10am Eastern ([Zoom link](https://upenn.zoom.us/j/98126042472?pwd=aHBPZDA2Tmd1aktZUUlDaW5BUjdHUT09))
* The Tuesday/Thursday section meets from noon-1:30pm Eastern ([Zoom link](https://upenn.zoom.us/j/99946920962?pwd=Z0liTlhNOUgwbHVuV3R5cTFLSVFYdz09))



Office hours (1-on-1 on [OHQ.io](https://ohq.io/courses/246))
<!--
: Mondays **3am-5am** Eastern (Samar Haider)
-->
: Mondays 10am-noon Eastern (Coco Zhao, Aditya Singh)
: Mondays noon-2pm Eastern (Kit Wiggin)
: Mondays 5-6pm Eastern (Roque Soto Castaneda)
: Mondays 5-7pm Eastern (Brian Wong)
: Mondays 8pm-10pm  Eastern(Hanbang Wang)
: Tuesdays 1-3pm Eastern (Artemis Panagopoulou)
: Tuesdays 7pm-9pm Eastern (John Wallison)
: Tuesdays 9pm-11pm Eastern (Yash Upadhyay)
: Wednesdays 10am-12pm Eastern (Xavier Lee)
: Wednesdays noon-2pm Eastern (Anna Orosz)
: Wednesdays 4pm-6pm Eastern (Ruochun Wang)
: Wednesday 8pm-10pm Eastern (Sherry Shi)
: Thursdays 9am-11am Eastern (Yue Yang)
: Thursdays 1pm-3pm Eastern (Yuxuan Huang)
: Thursdays 5pm-7pm Eastern (Viranchi Patel)
: Fridays 9am-11am Eastern (Zhi Zheng)
: Fridays noon-2pm Eastern (Lisa Zhao and David Wang)
: Fridays 2pm-4pm Eastern (Amy Guo and Harry Wang)
: Fridays 4pm-6pm Eastern (Ruochun Wang)
: Fridays 8pm-10pm Eastern (Enri Kina)
: Saturdays 8am-10am Eastern (Helen Jin)
: Saturdays 8:30am-10:30am Eastern (Aditya Singh)
: Saturdays 2pm-4pm Eastern (Roque Soto Castaneda)
: Saturdays 7pm-9pm Eastner (Xingyu Fu)
: Sundays 3pm-5pm Eastern (Roque Soto Castaneda)
: Sundays 6pm-8pm (Steven Wang)
: Sundays 7pm-9pm (Songyu Eve Yan)

Group Office Hours (Recorded)
: Fridays 2pm-3pm Eastern (Chris Callison-Burch)










Textbooks
: Required: __Artificial Intelligence: A Modern Approach (4th edition) by Russel and Norvig.__ Note that the 4th edition adds substantial new material over the 3rd edition, so you should buy the 4th edition.  You can [buy the textbook on Amazon](https://www.amazon.com/Artificial-Intelligence-A-Modern-Approach/dp/0134610997/) or from the [UPenn bookstore](https://upenn.bncollege.com/shop/upenn/page/find-textbooks), where you can rent the digital version for $40.  
: Supplemental: __Speech and Language Processing (3rd ed. draft) by Jurafsky and Martin__.  This textbook is currently [free online](https://web.stanford.edu/~jurafsky/slp3/) while the textbook authors are revising it to write their 3rd edition.  We will use it in the last third of the course. 


Materials for Extra Credit Assignments
: In addition to the normal homework assignments, we will have a series of optional extra credit assignments that use programmable toy R2D2s.  These assignments can be done in groups.  Each extra credit homework assignment if worth up to about 1% towards your final grade.  The total amount of extra credit earned will be divided among each student in a group (so students in a large group get less extra credit than students in smaller groups to refelct the effort done).
: You can borrow one of the R2D2 robots from us.  It must be returned at the end of the semester in good working order, or you will have to pay $100 to replace it. 

<!--
: If you are outside of Philadelphia, you can purchase a __Sphero R2D2__.  Currently, you can buy the robot for about $100 on [Amazon](https://www.amazon.com/Sphero-R201ROW-R2-D2-App-Enabled-Droid/dp/B071KSR86B/) or $80 from [Walmart.com](https://www.walmart.com/ip/Sphero-R2-D2-App-Enabled-Droid/707617540).  If you live outside the USA, you may need to use a [3rd party shipping service](https://planetexpress.com/stores/walmart/).
: If you live outside of Philadelphia, you will also need a Raspberry Pi Sensor Pack that the TAs assembled from parts. We will send it to you if [you provide your address on this form](https://docs.google.com/forms/d/e/1FAIpQLSdGu_0Qms_RxA42QCZY0A_PrJFPNgXrVENYmZTAclrj5ZKoww/viewform?usp=sf_link).
-->

Grading 
: * 70% Homework Assignments
* 30% Exams and Quizzes 
	* 10% for weekly quizzes (equally weighted)
	* 10% for midterm 1
	* 10% for midterm 2
* Up to 3-5% in Optional Extra Credit
: The course is not curved.  Your overall score is computed as _0.3 * exam score + 0.7 * homework score_.  All homeworks are equally weighted. Here is  how letter grades are assigned based on your overall score:
: | Score	| Grade   |
|-------|---------| 
| ≥ 97 | A+| 
| 93-97	| A| 
| 90-93	| A-| 
| 87-90	| B+| 
| 83-87	| B| 
| 80-83	| B-| 
| 75-80	| C+| 
| 70-75	| C| 
| 65-70	| C-| 
| 50-65	| D| 
| below 50	| F |

Differences between 421 and 521
: There is roughly one homework assignment per week, aside from weeks with exams.  Students enrolled in CIS 421 may skip one HW assignment, or they may discard their lowest scoring HW assignment.  You do not get late days back on the homework that you discard.  Students enrolled in CIS 521 must complete all HW assignments and cannot discard their lowest scoring assignment.


Collaboration Policy
: Quizzes and exams must be completed on your own without help from others.  For quizzes or exams that are open notes or allow a "cheatsheet", you must create the notes yourself and not use anyone else's notes.  Since exams are sometimes administered on different days, you should not discuss the exam with anyone else in the course until after the scores have been released.
: Unless otherwise noted, you are not allowed to work in groups on the homework assignments. You can discuss homework problems with others (you must explicitly list who you discussed problems with on each homework submission), but   *all code must be your own independent work.*  You are not allowed to upload your code to publicly accessible places (like public github repositories), and you are not allowed to access anyone else's code.  If you discover someone else's code online, please report it to the course staff via a private note on Piazza. 



Late Day Policy
: Each student has 5 free "late days".  Homeworks can be submitted at most two days late.  If you are out of late days, then you will not be able to get credit for subsequent late assignments. One "day" is defined as anytime between 1 second and 24 hours after the homework deadline. The intent of the late day policy it to allow you to take extra time due to unforseen circumstances like illnesses or family emergencies, and for forseeable interruptions like on campus interviewing and religious holidays.  You do not need to ask permission to use your late days.  No additional late days are granted. 

