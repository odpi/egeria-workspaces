# Dr.Egeria - designing data - part 2
## Adding information

As data professionals, we often need to design data to be collected, processed, and shared with others.
The Egeria Data Designer module has been designed to support this. Using the features of data designer we can
define and refine:

* Data Structures - a composition of data fields (and data structures) that we work with as a unit. For instance, in
a clinical trial, each measurement record we receive will conform to a data structure.
* Data Fields - the building blocks of data structures - for example, in a clinical trial data structure we might find data fields for health measurements, a time and date when the measurements were made and a patient identifier.
* Data Classes - data classes contain a set of rules that describe the allowable values of a kind of data. For instance, when we we receive new data, perhaps we expect a clinical trial measurement record, then we will often want to validate that it conforms to our expectations; that the value of each field, conforms to the data class specification.
Similarly, if we receive some data and aren't sure what it is, we can compare the values we have received with this same set of rules to propose what kind of data it might be.

These are basic building blocks. The following diagram shows how these building blocks come together in a simple example. The ficticious Coco Pharmaceuticals company
is running a drug trial to measure the effectiveness of their experimental treatment of Teddy Bear Drop Foot. Each hospital participating in the trial provides
weekly clinical data records. The clinical trial has established the following data specification to exchange this weekly measurement data.

* A data structure named `TBDF-Incoming Weekly Measurement Data` that is composed of:
* Data Field: Date
* Data Field: PatientId
* Data Field: AngleLeft
* Data Field: AngleRight

* The data field `PatientId` is composed of two sub-fields
* Data Field: HospitalId
* Data Field: PatientNumber

Dr.Egeria allows us to easily sketch this out, and then refine the definitions incrementally as we work through the design.
So lets begin. First we will define the `TBDF-Incoming Weekly Measurement Data` data structure. We will then Don't Create the new data fields.

___


# Update Data Structure

## Data Structure Name 

TBDF-Incoming Weekly Measurement Data

## GUID
c3f75f00-10c2-46f3-b4b3-048ef40bfc65

## Qualified Name
DataStruct::TBDF-Incoming Weekly Measurement Data

## Description
This describes the weekly measurement data for each patient for the Teddy Bear drop foot clinical trial.

## Data Fields


## Data Specification


## Namespace


## Version Identifier


## Extended Properties
{}

## Additional Properties
{}



> Note: While not required, it is good practice to end each Dr.Egeria command with a `___` so that a markdown
> seperator is displayed between commands. It improves the readability.


# Update Data Field

## Data Field Name 

Date

## GUID
b0a66e94-8473-42f7-91bb-a92d389c1ba6

## Qualified Name
DataField::Date

## Description
A date of the form YYYY-MM-DD

## Assigned Meanings


## Data Type
string

## Data Class


## Is Nullable
True

## Minimum Length
0

## Length
0

## Precision
0

## Ordered Values
False

## Sort Order
UNSORTED

## Parent Names


## Extended Properties
{}

## Additional Properties
{}

## Data Dictionaries


## Data Structures




___




# Update Data Field

## Data Field Name 

PatientId

## GUID
c442adde-2c24-4b90-9dfb-111dbdf1b357

## Qualified Name
DataField::PatientId

## Description
Unique identifier of the patient

## Assigned Meanings


## Data Type
string

## Data Class


## Is Nullable
True

## Minimum Length
0

## Length
0

## Precision
0

## Ordered Values
False

## Sort Order
UNSORTED

## Parent Names


## Extended Properties
{}

## Additional Properties
{}

## Data Dictionaries


## Data Structures




___




# Update Data Field

## Data Field Name 

AngleLeft

## GUID
9f525f95-646f-4abf-874d-5de0b131a9ce

## Qualified Name
DataField::AngleLeft

## Description
Angle rotation of the left leg from vertical

## Assigned Meanings


## Data Type
string

## Data Class


## Is Nullable
True

## Minimum Length
0

## Length
0

## Precision
0

## Ordered Values
False

## Sort Order
UNSORTED

## Parent Names


## Extended Properties
{}

## Additional Properties
{}

## Data Dictionaries


## Data Structures




___




# Update Data Field

## Data Field Name 

AngleRight

## GUID
9c6d96f2-724b-4109-b513-f978d911fe34

## Qualified Name
DataField::AngleRight

## Description
Angle rotation of the left leg from vertical

## Assigned Meanings


## Data Type
string

## Data Class


## Is Nullable
True

## Minimum Length
0

## Length
0

## Precision
0

## Ordered Values
False

## Sort Order
UNSORTED

## Parent Names


## Extended Properties
{}

## Additional Properties
{}

## Data Dictionaries


## Data Structures




___




# Update Data Field

## Data Field Name 

HospitalId

## GUID
7f33b0a5-fe31-4fd3-a7ec-90dd7520cfa8

## Qualified Name
DataField::HospitalId

## Description
Unique identifier for a hospital. Used in forming PatientId.

## Assigned Meanings


## Data Type
string

## Data Class


## Is Nullable
True

## Minimum Length
0

## Length
0

## Precision
0

## Ordered Values
False

## Sort Order
UNSORTED

## Parent Names


## Extended Properties
{}

## Additional Properties
{}

## Data Dictionaries


## Data Structures




___




# Update Data Field

## Data Field Name 

PatientNumber

## GUID
ed77dfa2-67ee-48b9-b724-515d54673653

## Qualified Name
DataField::PatientNumber

## Description
Unique identifier of the patient within a hospital.

## Assigned Meanings


## Data Type
string

## Data Class


## Is Nullable
True

## Minimum Length
0

## Length
0

## Precision
0

## Ordered Values
False

## Sort Order
UNSORTED

## Parent Names


## Extended Properties
{}

## Additional Properties
{}

## Data Dictionaries


## Data Structures




___


# REPORTING
We can also use Dr.Egeria Commands to report on the Data Structures and Data Fields that we just created. Here
we request a simplified list form of the output.
___


# `Data Structures` with filter: `*`

# Data Structures Table

Data Structures found from the search string: `All`

| Structure Name | Qualified Name | Namespace | Version | Description | 
|-------------|-------------|-------------|-------------|-------------|
| TBDF-Incoming Weekly Measurement Data |  [DataStruct::TBDF-Incoming Weekly Measurement Data](#c3f75f00-10c2-46f3-b4b3-048ef40bfc65)  |  |  | This describes the weekly measurement data for each patient for the Teddy Bear drop foot clinical trial. | 



# `Data Fields` with filter: `*`

# Data Fields Table

Data Fields found from the search string: `<class 'filter'>`

| Field Name | Qualified Name | Data Type | Description | 
|-------------|-------------|-------------|-------------|
| AngleRight |  [DataField::AngleRight](#9c6d96f2-724b-4109-b513-f978d911fe34)  | string | Angle rotation of the left leg from vertical | 
| HospitalId |  [DataField::HospitalId](#7f33b0a5-fe31-4fd3-a7ec-90dd7520cfa8)  | string | Unique identifier for a hospital. Used in forming PatientId. | 
| PatientId |  [DataField::PatientId](#c442adde-2c24-4b90-9dfb-111dbdf1b357)  | string | Unique identifier of the patient | 
| Date |  [DataField::Date](#b0a66e94-8473-42f7-91bb-a92d389c1ba6)  | string | A date of the form YYYY-MM-DD | 
| AngleLeft |  [DataField::AngleLeft](#9f525f95-646f-4abf-874d-5de0b131a9ce)  | string | Angle rotation of the left leg from vertical | 
| PatientNumber |  [DataField::PatientNumber](#ed77dfa2-67ee-48b9-b724-515d54673653)  | string | Unique identifier of the patient within a hospital. | 

# Building on what we have done
One of the interesting features of Dr.Egeria, is that we can take the results of processing a Dr.Egeria command as the
starting point for refining the information we provided. This is convenient, because when we generate the command output,
we transform the `Create` commands into `Update` commands. We also add some additional information that Egeria derived for us.

## Next Steps
For our next steps, we will copy the file produced in the first step into a new file called `dr_egeria_data_designer_2.md`
Please open that file when you are ready to continue.
# Provenance

* Results from processing file dr_egeria_data_designer_1.md on 2025-06-25 01:39
