# emotions.module.eLL.CMS

Emotions Module for the eLL-CMS Sytems

### Author: Daniel Felipe Gomez Aristizabal

### Tutor: Coromoto Leon Hernandez

### Co-Tutor: Rafael Herrero Alvarez


## Demo

If you are student from the University of La Laguna and you want to see the system working you can access to the following link:




## Description

This repository contains the Emotions Module for the eLL-CMS Systems. This work is part of my Thesis Project for the Degree of Computer Science at the University of La Laguna. The system is bases on the [Contest Management System (CMS)](https://github.com/cms-dev/cms/tree/v1.4) a distributed system for running and (to some extent) organizing a programming contest.

The repository include the diferents modification to able the system to measure the emotions during the process of solving activities of programming to help develop the computational thinking of the students.

With the modification we add the following features:

- **Creation of a new entity called Emotion** to store the emotions of the students.

![Emotion model](./images_readme/emotion_model.png)

- **Creation of a new entity called FormEmotion** to store forms to measure the emotions of the students.

![Form Emotion model](./images_readme/formemotion_model.png)

- **Creation of a new relationships between the old entities and the new entities** to store the emotions of the students and access correctly to the information.

![Creation of a new relationships between the old entities and the new entities](./images_readme/relationships.png)


- **Creation of many diferents screens to offer different ways to manage the emotions and the measures of the emotions**.

![alt text](./images_readme/example-1.png)
![alt text](./images_readme/example-2.png)

- **Creation of forms to measure the emotions of the students** the administrators can create forms to measure the emotions of the students. This forms could be added importing a JSON file with the structure of the form. Other way is to creating the form in the system anwsering the questions to indicate the type of each question, a optional statement and a optional image. 

![Creation of forms to measure the emotions of the students](./images_readme/creation_forms.png)

- **Exportation of the forms created** the administrators can export the forms created in the system in a JSON file. The JSON file contains the structure of the form created.


![Exportation of the forms created](./images_readme/export_form.png)

- **Dinamically representation of the forms created** the forms created are represented in the system in a dinamically way. The system is able to represent the forms created in a way that the students can anwser the questions of the form.


![Dinamically representation of the forms created*](./images_readme/form_preview.png)

- **Creation of diferents tools to view the measurents obteined** the system offer many ways to view the measurents obteined. The administrators can view the measurents in a table, in a graph or in a pie chart. The system offer the possibility to filter the measurents by the date of the measurents, the form of the measurents, the student of the measurents and the activity of the measurents.

![Creation of diferents tools to view the measurents obteined](./images_readme/result_context.png)

## Installation

How we say before, this repository is the result of the modification proposed in my TFG for that reason the installation of this repository and the CMS are explained in the memory of the TFG. The memory of the TFG is in spanish and is available in the TFG's repository of the University of La Laguna. 

