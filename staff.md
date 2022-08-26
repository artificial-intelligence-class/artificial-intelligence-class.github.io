---
layout: default
title: CIS 521 Staff
active_tab: staff
---

<style>
/* The flip card container - set the width and height to whatever you want. We have added the border property to demonstrate that the flip itself goes out of the box on hover (remove perspective if you don't want the 3D effect */
.flip-card {
  background-color: transparent;
  width: 250px;
  height: 250px;
  border: 1px solid #f1f1f1;
  perspective: 1000px; /* Remove this if you don't want the 3D effect */
}

/* This container is needed to position the front and back side */
.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  text-align: center;
  transition: transform 0.8s;
  transform-style: preserve-3d;
}

/* Do an horizontal flip when you move the mouse over the flip box container */
.flip-card:hover .flip-card-inner {
  transform: rotateY(180deg);
}

/* Position the front and back side */
.flip-card-front, .flip-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  -webkit-backface-visibility: hidden; /* Safari */
  backface-visibility: hidden;
}

/* Style the front side (fallback if image is missing) */
.flip-card-front {
  background-color: #bbb;
  color: black;
}

/* Style the back side */
.flip-card-back {
  background-color: #bbb;
  color: black;
  transform: rotateY(180deg);
}
</style>



<div class="container-fluid">
  <div class="row">
  {% for staff in site.data.staff %}
      <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom: 20px; height: 350px;">
        <ul class="list-unstyled">
          <li>
            {% if staff.pic %}
            <div class="flip-card">
              <div class="flip-card-inner">
                <div class="flip-card-front">
                  <img src="assets/img/staff/{{ staff.pic }}" alt="{{ staff.name }}" style="height: 100%; width: 100%; max-height: 250px; max-width: 250px">
                </div>
                <div class="flip-card-back">
                  <img src="assets/img/staff/{{ staff.ai_pic }}" alt="AI generated portrait of {{ staff.name }}" style="height: 100%; width: 100%; max-height: 250px; max-width: 250px">
                </div>
              </div>
            </div>
            {% else %}
              <img src="assets/img/kermit.png" class="img-circle" style="height: 100%; width: 100%; max-height: 250px; max-width: 250px">
            {% endif %}
          </li>
          {% if staff.url %}
            <li><b><a href="{{ staff.url }}">{{ staff.name }}</a></b> {% if staff.pronouns %}({{staff.pronouns}}){% endif %}</li>
          {% else %}
            <li><b>{{ staff.name }}</b> {% if staff.pronouns %}({{staff.pronouns}}){% endif %}</li>
          {% endif %}
          {% if staff.extra_title %}<li><em>{{ staff.extra_title }}</em></li>{% endif %}
          {% if staff.email %}<li><b>Email:</b><code>{{ staff.email }}</code></li>{% endif %}
       	  {% if staff.office_hours %}<li><b>Office Hours:</b> {{ staff.office_hours | inline_markdownify }}</li>{% endif %}
          {% if staff.location %}<li><b>Location:</b> {{ staff.location | inline_markdownify }}</li>{% endif %}
        </ul>
      </div>
    {% endfor %}
  </div>
</div>
