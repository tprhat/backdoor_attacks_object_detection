# backdoor_attacks_object_detection

Msc Thesis: Backdoor Attacks Upon Object Detection Neural Networks

Backdoor was implemented as trigger which was a chessboard PNG.

The triggers were:
- Global trigger: changes all classes in a photo to the desired class "person"
- Misclassification trigger: changes the class of an object to the desired class "person"
- Creation trigger: creates a bounding box of class "person"
- Deletion trigger: removes bounding box and label around class "person"

If you want to read more, check out the "Diplomski_rad.pdf" file.