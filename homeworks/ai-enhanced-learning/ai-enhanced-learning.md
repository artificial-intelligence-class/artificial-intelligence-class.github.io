---
layout: default
img: ai_methodology.png
img_link: http://chatgpt.com
caption: Let's use AI!
title: AI-Enhanced Learning 
type: Homework
number: 1
active_tab: homework
release_date: 2025-01-28
due_date: 2025-02-05 23:59:00EDT
transcripts: 
    - 
      name: Transcript of Lecture 1 on AI in Philosophy and SciFy
      url: lecture-1.txt
    - 
      name: Transcript of Lecture 2 on AGI and Rational Agents
      url: lecture-2.txt
materials:
    -
      name: René Descartes (1637) "Discourse on the Method (Part Five, pages 97-100)"
      url: https://en.wikisource.org/wiki/Discourse_on_the_Method/Part_5
    - 
      name: Alan Turing (1950) "Computing Machinery and Intelligence" 
      url: https://courses.cs.umbc.edu/471/papers/turing.pdf
    - 
      name: John R. Searle (1980) "Minds, Brains, and Programs"
      url: https://web-archive.southampton.ac.uk/cogprints.org/7150/1/10.1.1.83.5248.pdf
    - 
      name: Daniel Dennett (1978) 'Where Am I?'
      url: https://thereader.mitpress.mit.edu/daniel-dennett-where-am-i/
models:
    - 
      name: ChatGPT
      url: https://chatgpt.com
    - 
      name: Claude
      url: https://claude.ai
    - 
      name: DeepSeek R1
      url: https://chat.deepseek.com/
    - 
      name: Gemini
      url: https://gemini.google.com
    - 
      name: Copilot
      url: https://copilot.microsoft.com/chats/
    - 
      name: NotebookLM
      url: https://notebooklm.google
submission_link: XXX
---

<!-- Check whether the assignment is ready to release -->
{% capture today %}{{'now' | date: '%s'}}{% endcapture %}
{% capture release_date %}{{page.release_date | date: '%s'}}{% endcapture %}
{% if release_date > today %} 
<div class="alert alert-danger">
Warning: this assignment is out of date.  It may still need to be updated for this year's class.  Check with your instructor before you start working on this assignment.
</div>
{% endif %}
<!-- End of check whether the assignment is up to date -->


<!-- Check whether the assignment is up to date -->
{% capture this_year %}{{'now' | date: '%Y'}}{% endcapture %}
{% capture due_year %}{{page.due_date | date: '%Y'}}{% endcapture %}
{% if this_year != due_year %} 
<div class="alert alert-warning">
Warning: this assignment is out of date.  It may still need to be updated for this year's class.  Check with your instructor before you start working on this assignment.
</div>
{% endif %}
<!-- End of check whether the assignment is up to date -->








{{page.type}} {{page.number}}: {{page.title}}
=============================================================

In this homework assignment, you will explore how AI systems can enhance learning and deepen your understanding of course material. You'll work with AI tools to process, analyze, and create educational content while developing critical thinking skills about AI's role in education.

## Objectives
- Transform lecture content into structured educational materials
- Engage critically with philosophical texts about AI
- Design assessment materials
- Envision the future of AI-enhanced educational tools



{% if page.models %}
<div class="alert alert-info">
You can pick one or more of these models to use for this homework:
<ul>
{% for item in page.models %}
<li><a href="{{item.url}}">{{ item.name }}</a></li>
{% endfor %}
</ul>
</div>
{% endif %}


## Part 1: Creating Enhanced Lecture Notes
Using an AI system, convert the transcripts from Lectures 1 and 2 into well-organized, textbook-style notes. Your notes should:
- Identify and bold key terms
- Include clear section headings and subheadings
- Incorporate relevant examples from the lectures
- Create a comprehensive glossary of technical terms and concepts



{% if page.transcripts %}
<div class="alert alert-success">
You can download the lecture transcripts here:
<ul>
{% for item in page.transcripts %}
<li><a href="{{item.url}}">{{ item.name }}</a></li>
{% endfor %}
</ul>
</div>
{% endif %}


## Part 2: Philosophical Analysis
Select readings from key philosophers discussed in Lecture 1 (Descartes, Turing, Searle, and Dennett). Working with the AI system:
- Generate summaries of the philosophical essays
- Connect the philosophical arguments to themes from the lectures
- Develop and pursue thoughtful questions that demonstrate critical engagement with the material
- Document your dialogue with the AI system about these topics


{% if page.materials %}
<div class="alert alert-warning">
You can download the philosophic essays here:
<ul>
{% for item in page.materials %}
<li><a href="{{item.url}}">{{ item.name }}</a></li>
{% endfor %}
</ul>
</div>
{% endif %}




## Part 3: Assessment Design
Create assessment materials that target key learning objectives from the lectures:

Multiple Choice Questions (create 5):
- Each question should include:
  - Clear question stem
  - One correct answer
  - 3-4 plausible distractors
  - Explanation of why the correct answer is right and why others are wrong

Short Answer Questions (create 5):
- Questions answerable in 1-2 sentences
- Sample answers demonstrating expected depth and specificity

Essay Question (create 2):
- Question requiring 1-2 paragraphs of analysis
- Sample answer showing expected depth and reasoning
- Detailed grading rubric with clear criteria

If you would like some tips on writing good assessment materials, you can look up [Bloom's Taxonomy](https://en.wikipedia.org/wiki/Bloom's_taxonomy).

## Part 4: Smart Textbook Concept
Develop a vision for an AI-enhanced "smart textbook" of the future.

Independent Analysis (your own words - don't use AI here):
- Write your initial ideas about features, benefits, and use cases
- Consider potential challenges and limitations
- Describe ideal user interactions

AI-Enhanced Proposal:
- Use AI to expand and refine your initial concepts
- Create a professional product brochure
- Optional: Include AI-generated illustrations

## Deliverables
1. Enhanced Lecture Notes (PDF)
   - Lecture 1 and 2 content
   - Glossary of terms
   - Documentation of which AI system(s) you used and how you prompted it to create your lecture notes

2. Philosophical Dialogue (PDF)
   - Complete dialogue transcript with AI
   - Analysis of philosophical connections
   - Reflection on insights gained

3. Assessment Materials (PDF)
   - Multiple choice questions with explanations
   - Short answer questions with sample responses
   - Essay question with rubric

4. Smart Textbook Proposal (PDF)
   - Initial concept development
   - Final product brochure
   - Optional illustrations


<table>
   {% for publication in page.readings %}
    <tr>
      <td>
	{% if publication.url %}
		<a href="{{ publication.url }}">{{ publication.title }}</a>
        {% else %}
		{{ publication.title }}
	{% endif %}
	{% if publication.authors %}	      
		- {{ publication.authors }}.
	{% endif %}
	{% if publication.year %}	
		{{ publication.venue }}  {{ publication.year }}.
	{% endif %}

	{% if publication.abstract %}
	<!-- abstract button -->
	<a data-toggle="modal" href="#{{publication.id}}-abstract" class="label label-success">Abstract</a>
	<!-- /.abstract button -->
	<!-- abstract content -->
	<div id="{{publication.id}}-abstract" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="{{publication.id}}">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
          <h4 class="modal-title" id="{{publication.id}}">{{publication.title}}</h4>
        </div><!-- /.modal-header -->
        <div class="modal-body">
        {{publication.abstract}}
        </div><!-- /.modal-body -->
	</div><!-- /.modal-content -->
	</div><!-- /.modal-dialog -->
	</div><!-- /.abstract-content -->
	{% endif %}
	{% if publication.bibtex %}
	<!-- bibtex button -->
	<a data-toggle="modal" href="#{{publication.id}}-bibtex" class="label label-default">BibTex</a>
	<!-- /.bibtex button -->
	<!-- bibtex content -->
	<div id="{{publication.id}}-bibtex" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="{{publication.id}}">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
          <h4 class="modal-title" id="{{publication.id}}">{{publication.title}}</h4>
        </div><!-- /.modal-header -->
        <div class="modal-body">
 	   <pre>{{publication.bibtex}}
           </pre>
        </div><!-- /.modal-body -->
	</div><!-- /.modal-content -->
	</div><!-- /.modal-dialog -->
	</div><!-- /.bibtex-content -->
	{% endif %}
</td></tr>
  {% endfor %}
</table>
