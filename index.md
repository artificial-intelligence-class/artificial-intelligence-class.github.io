---
title: CIS 421/521 - Artificial Intelligence - University of Pennsylvania
layout: default
img: R2D2.png
active_tab: main_page 
---



<div class="alert alert-danger" markdown="1">
To get a permit for CIS 421/521, you should [sign yourself up for the CIS waitlist](https://forms.cis.upenn.edu/waitlist/index.php).  After you've added yourself to the waitlist, you'll get assigned a category based on your degree and how many years you have left at Penn.  If you have a question about the waitlist system you can email Lee Dukes ldukes@seas.upenn.edu.  

In order to be considered for a permit for the course, you must complete the first assignment by its due date.
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

<div class="alert alert-success" markdown="1">
[When you borrow one of the programmable toy R2D2s for the semester, please fill out this Robot Checkout Form.](https://docs.google.com/forms/d/e/1FAIpQLSeVrCvG_2zcb2bPdn0bor61EOTzzqesI748l1pG4u9TqJ_GgQ/viewform?usp=sf_link)
</div>



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

Instructor
: [Chris Callison-Burch](https://www.cis.upenn.edu/~ccb/)

Discussion Forum
: [Piazza](https://piazza.com/upenn/fall2020/cis521)

Time and place
: In Fall 2020, the course will be all online.
: Lectures will be [broadcast live on Zoom](https://upenn.zoom.us/j/97517317746?pwd=dlZSZTZXd1ZXaDhqeUhDK251TTFndz09) on Tuesdays and Thursdays from noon-1:30pm Eastern. Recordings will be made available shortly after the live lectures. 
: The first day of class is Tuesday, September 1, 2020.
: The final day of class is Tuesday, December 22, 2020.

Office hours 
: Office hours will be held in [Gather Town](https://gather.town/aQMGI0l1R8DP0Ovv/penn-cis) in 3401 Walnut outside of room 463C.
: The first day of office hours will be Monday, September 7.
: Monday 11am-1pm Eastern - Chris
: Monday 4:30pm-6:30pm Eastern – Eddie
: Tuesday 3am-5am Eastern / 3pm-5pm China - Hanbang 
: Tuesday 9am-11am Eastern - Yue
: Tuesday 10am-12pm Eastern - Bharath
: Tuesday 2pm-4pm Eastern- Chenyu
: Tuesday 4pm-6pm Eastern - Aditya
: Tuesday 6pm-8pm Eastern - Joe
: Wednesday 12:30pm-2:30pm Eastern - Daniel
: Wednesday 2:30pm-4:30pm Eastern - Halley
: Friday 3pm-5pm Eastern - Lisa


Textbooks
: Required: __Artificial Intelligence: A Modern Approach (4th edition) by Russel and Norvig.__ Note that the 4th edition adds substantial new material over the 3rd edition, so you should buy the 4th edition.  You can [buy the textbook on Amazon](https://www.amazon.com/Artificial-Intelligence-A-Modern-Approach/dp/0134610997/) or from the [UPenn bookstore](https://upenn.bncollege.com/shop/upenn/page/find-textbooks), where you can rent the digital version for $40.  
: Supplemental: __Speech and Language Processing (3rd ed. draft) by Jurafsky and Martin__.  This textbook is currently [free online](https://web.stanford.edu/~jurafsky/slp3/) while the textbook authors are revising it to write their 3rd edition.  We will use it in the last third of the course. 



Materials for Extra Credit Assignments
: In addition to the normal homework assignments, we will have a series of optional extra credit assignments that use programmable toy R2D2s.  These assignments can be done in pairs.  Each extra credit homework assignment if worth up to about 1% of your overall grade.
: If you are in Philadelphia, you can borrow one of the R2D2 robots from us.  It must be returned at the end of the semester in good working order, or you will have to pay $100 to replace it. 
: If you are outside of Philadelphia, you can purchase a __Sphero R2D2__.  Currently, you can buy the robot for about $100 on [Amazon](https://www.amazon.com/Sphero-R201ROW-R2-D2-App-Enabled-Droid/dp/B071KSR86B/) or $80 from [Walmart.com](https://www.walmart.com/ip/Sphero-R2-D2-App-Enabled-Droid/707617540).  If you live outside the USA, you may need to use a [3rd party shipping service](https://planetexpress.com/stores/walmart/).
: If you live outside of Philadelphia, you will also need a Raspberry Pi Sensor Pack that the TAs assembled from parts. We will send it to you if [you provide your address on this form](https://docs.google.com/forms/d/e/1FAIpQLSdGu_0Qms_RxA42QCZY0A_PrJFPNgXrVENYmZTAclrj5ZKoww/viewform?usp=sf_link).



Grading 
: 70% Homework Assignments
: 30% Exams and Quizzes
: Up to 3-5% in Optional Extra Credit
: The course is not curved.  Your overall score is computed as _0.3 * exam score + 0.7 * homework score_.  All homeworks are equally weighted. Here is  how letter grades are assigned based on your overall score:
: | Score	| Grade   |
|-------|---------| 
|$$>$$ 97 | A+| 
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
: Unless otherwise noted, you are not allowed to work in groups on the homework assignments. You can discuss homework problems with others (you must explicitly list who you discussed problems with on each homework submission), but   *all code must be your own independent work.*  You are not allowed to upload your code to publicly accessible places (like public github repositories), and you are not allowed to access anyone else's code.  If you discover someone else's code online, please report it to the course staff via a private note on Piazza. 


Late Day Policy
: (TO BE UPDATED)
: Each student has five free "late days".  Homeworks can be submitted at most two days late.  If you are out of late days, then you will not be able to get credit for subsequent late assignments. One "day" is defined as anytime between 1 second and 24 hours after the homework deadline. The intent of the late day policy it to allow you to take extra time due to unforseen circumstances like illnesses or family emergencies, and for forseeable interruptions like on campus interviewing and religious holidays.  You do not need to ask permission to use your late days.  No additional late days are granted. 

