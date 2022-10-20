# College
A database application using a typical college schema.

For this database application, consider a UNIVERSITY database that keeps track of students and their majors, transcripts, and registration as well as of the university’s course offerings. The database also keeps track of the sponsored research projects of faculty/graduate students and so on.

The schema used as a blueprint for the development of this application uses an EER model for the representation of major entities present in typical university environment and the corresponding relationship between these entities. This schema can be found in the project root directory with the name "schema.png".


Shipped with this database application are these core functionalities:
User-Authentication-System, User-Permissions-Management, 
Activities Logging, 
Internationalisation.
Interface customization.


There are three group of user for this application, each group with it designated list of permission:

Admin(the superuser) -> have all permission, can add change, view and delete data in any table except for logging, where superuser only have view permission.

Editor -> have add, change, view and delete permission on selected tables.

Attendant -> only have view permission on selected tables.



