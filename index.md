---
title: CIS 4210/5210 - Artificial Intelligence - University of Pennsylvania
layout: default
img: R2D2.png
active_tab: main_page 
---

<!--
<div class="alert alert-danger" markdown="1">
**Waitlist update**: I added a second session with addition 200 spaces to the course.  That session meets Mondays and Wednesdays at 8:30am-10am in Heilmeier auditorium.  You can get a permit by signing up on [CIS Waitlist System](https://forms.cis.upenn.edu/waitlist/index.php) for CIS4210/5210-402.

For  questions about the waitlist or registration, please contact Lee Dukes - ldukes@seas.upenn.edu.
</div>
-->

<div class="alert alert-danger" markdown="1">
You don't need to contact the course instructor to get permissions to register for CIS 4210/5210.  Here are the steps that you should follow:

**Step 1:** Decide which version of the course you want to enroll in.  4210 is for undergradutes who are not planning on doing a masters (submatting).  5210 is for master's students including students planning on submatriculating, and for PhD students.


**Step 2:** You should [request permission for the course in the Path@Penn tool](https://apps.srfs.upenn.edu:44306/secure/Pennant-Training/Path-Request-Permission-to-Take-a-Class.pdf).  Here's a [short video showing how to use the new Path@Penn interface](https://urldefense.com/v3/__https://drive.google.com/file/d/1zyf21DYVYWzLRsp-y09hRaqG-QhFMf-5/view?usp=sharing__;!!IBzWLUs!Q0vTJ4XhWQYBml_TICPzVBEnB-TfUKZjoxFeLDlOjoQxGJ37ptjONZf704stRJ8mXG8d7BocetPqLTKeIrEY$).

**Step 3:** The following day you'll be asked to login to the CIS Waitlist system to answer some questions.  You can read more information about the [CIS Waitlist system here](https://advising.cis.upenn.edu/waitlist/).

**Step 4:** Be Patient. The first batch of 300 permits have been issued, but we plan on issuing another batch after the semester begins.  

**Step 5:** If you have been approved for the course you will be contacted via email with how you can claim permission for the course in the Path@Penn tool and register.

For more info about CIS 4210/5210, check out the [course homepage](http://artificial-intelligence-class.org).

If you're hoping to take the course but do not yet have a permit, you should complete the first homework assignment and submit it before the deadline. 
</div> 



<div class="alert alert-success" markdown="1">
After you've added yourself to the waitlist, you'll get assigned a category based on your degree and how many years you have left at Penn.  I have increased the enrollment to allow 400 students in the class, so hopefully there will be enough room for everyone who is interested!
</div>

<div class="alert alert-info" markdown="1">
This course is programming intensive, and requires prior Python experience and previous computer sceince courses in data structures and algorithms.  If you'd like to self-assess whether your background is appropriate, you can try out the first few homework assignments prior to the start of the class.
</div>





<!--
<div class="alert alert-info" markdown="1">
The course is done!  Please fill out this [end of semester survey](https://docs.google.com/forms/d/e/1FAIpQLSfYzkk9MD5WOda8WgUgXeDEDy06gUunApho2Me4nYoLXzgufQ/viewform?usp=sf_link) to give us feedback on how to improve the class next year.  If you loved the class, and would like to apply to be a TA, please fill out [this application](https://docs.google.com/forms/d/e/1FAIpQLSeGM7uegYNxf0pY6T2lOhMpUosnVnH3c1woZ10IcFJ18IKN-A/viewform?usp=sf_link).  If you'd like to volunteer for activities  with my research group you can [fill out this form](https://docs.google.com/forms/d/e/1FAIpQLScWgXblpIkADdO_K3PQIgm4LAGz0o-XEByPIVJg6_ObxZVAPQ/viewform).
</div>


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
: CIS 4210/5210 - Artificial Intelligence

Prerequeisites
: CIS 121 (for undergraduates)
: CIT 594 and CIT 596 (for MCIT students)
: A data structure and algorithms course, plus substantial programming experience (for everyone)

Instructor
: [Chris Callison-Burch](https://www.cis.upenn.edu/~ccb/)

Discussion Forum
: XXX

Time and place
: In Fall 2022, the course will be in-person in Myerson B1 and broadcast live via Zoom. You are not obligated to attend in person.  Everyone is welcome to watch the videos from home.
: All lecture materials will be recorded and uploaded for students wishing to participate remotely.  We also have [pre-recorded lectures available for review](modules.html).
: The first day of class is Tuesday, August 30, 2022.
: The first day of office hours will be Tuesday, September 6, 2022.
: The final day of class is Thursday, December 8, 2022.
* The class meets on Tuesday/Thursday from noon-1:30pm Eastern.



<!--
: Mondays **3am-5am** Eastern (Samar Haider)
-->

Office hours (1-on-1 on [OHQ.io](https://ohq.io/courses/246))
: TBD

Group Office Hours (Recorded)
: TBD (Chris Callison-Burch)







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

Differences between 4210 and 5210
: There is roughly one homework assignment per week, aside from weeks with exams.  Students enrolled in CIS 4210 may skip one HW assignment, or they may discard their lowest scoring HW assignment.  You do not get late days back on the homework that you discard.  Students enrolled in CIS 5210 must complete all HW assignments and cannot discard their lowest scoring assignment.  **If you are an undergraduate who is considering submatriculating into the master's program then you should enroll in CIS 5210.**



Collaboration Policy
: Quizzes and exams must be completed on your own without help from others.  For quizzes or exams that are open notes or allow a "cheatsheet", you must create the notes yourself and not use anyone else's notes.  Since exams are sometimes administered on different days, you should not discuss the exam with anyone else in the course until after the scores have been released.
: Unless otherwise noted, you are not allowed to work in groups on the homework assignments. You can discuss homework problems with others (you must explicitly list who you discussed problems with on each homework submission), but   *all code must be your own independent work.*  You are not allowed to upload your code to publicly accessible places (like public github repositories), and you are not allowed to access anyone else's code.  If you discover someone else's code online, please report it to the course staff via a private note on Piazza. 



Late Day Policy
: Each student has 5 free "late days".  Homeworks can be submitted at most two days late.  If you are out of late days, then you will not be able to get credit for subsequent late assignments. One "day" is defined as anytime between 1 second and 24 hours after the homework deadline. The intent of the late day policy it to allow you to take extra time due to unforseen circumstances like illnesses or family emergencies, and for forseeable interruptions like on campus interviewing and religious holidays.  You do not need to ask permission to use your late days.  No additional late days are granted. 

