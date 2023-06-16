● [El PIG debe subirse a un repositorio GIT público en la nube.](https://github.com/Nhg1973/inscripcionCodoaCodo.git)

● [El proyecto deberá poseer al menos una aplicación de Django](gestion_cursos)

●[ Deben existir al menos 3 rutas distintas.](gestion_publicas/urls.py)

● [Debe existir al menos una vista parametrizada.](gestion_cursos\urls.py)

● Se deben utilizar templates que cumplan con las siguientes características:

• [Debe haber al menos un template asociado a una vista.](gestion_publicas\views.py)
• [Debe existir al menos una relación de herencia entre los templates.](gestion_personas\templates\gestion_personas\dashboardAlumnos.html)
• [Debe existir al menos un filtro aplicado.](gestion_personas\templates\gestion_personas\dashboardAlumnos.html)
• [Debe existir al menos un template que utilice archivos estáticos (js, css, etc).](gestion_personas\templates\gestion_personas\dashboardDocentes.html)

● Se deben utilizar Django Forms que cumplan con las siguientes características:

• [Al menos un formulario debe poseer validaciones en el front-end y en el back-end]([label](gestion_personas/formrs/user_registration_form.py))
• [Debe haber al menos un formulario asociado a un template.](gestion_personas\views.py)
• [Debe haber al menos un formulario basado en clases.](gestion_personas\formrs\loginForm.py)
• [Debe haber al menos un formulario asociado a un modelo.](gestion_personas\formrs\create_categoria_form.py)
● [Deben existir al menos dos modelos distintos.](gestion_personas\models.py)

● [En los modelos generados, debe haber al menos una relación de uno a muchos y una relación de muchos a muchos.](gestion_cursos\models.py)

● El proyecto debe funcionar utilizando un servidor de base de datos local dentro de los
soportados (en el curso se recomienda PostgreSQL), y debe poseer las migraciones
necesarias para su funcionamiento (no se permite utilizar SQLLite).

● Debe poder accederse al admin de Django y al menos los modelos que poseen la relación
muchos a muchos deben poder administrarse del mismo.

● El proyecto debe poseer al menos una página a la que solo se pueda acceder mediante

autenticación y la misma debe ser validada tanto en el front-end como el back-end.
