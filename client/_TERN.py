from rdflib.term import URIRef
from rdflib.namespace import DefinedNamespace, Namespace


class TERN(DefinedNamespace):
    """
    DESCRIPTION_EDIT_ME_!
    Generated from: SOURCE_RDF_FILE_EDIT_ME_!
    Date: 2022-03-08 01:39:08.339590
    """

    _NS = Namespace("https://w3id.org/tern/ontologies/tern/")

    Attribute: URIRef  # A property-value pair. Same modelling pattern as [schema:PropertyValue](https://schema.org/PropertyValue).
    Boolean: URIRef  # Class to encapsulate a true-or-false value
    CategoricalValue: URIRef  # None
    CosmOzStation: URIRef  # CosmOz is the Australian Cosmic-Ray Neutron Soil Moisture Monitoring Network Beginning in October 2010, CSIRO Land and Water installed cosmic-ray probes at a number of locations around Australia to form the inaugural CosmOz network. These sites were established at instrumented research sites operated by CSIRO and University collaborators to test and validate the operation of this new technology. These novel probes use cosmic rays originating from outer space to measure average soil moisture over an area of about 30 hectares to depths in the soil of between 10 to 50 cm. This constitutes a quantum leap over conventional on-ground soil moisture sensing technology that can only measure soil moisture content within small volumes of soil. Each system is comprised of a data logger, neutron detector, satellite telemetry, tipping bucket rain gauge, temperature humidity and pressure sensors and three surface moisture (TDR) probes. The system requires minimal maintenance and is powered by a solar charging system. The entire system is installed on a single mast. Data is logged and transmitted every 60 minutes to the CosmOz database.
    Dataset: URIRef  # A collection of data, published or curated by a single agent, and available for access or download in one or more representations.
    Date: URIRef  # None
    DateTime: URIRef  # None
    Deployment: URIRef  # Describes the Deployment of one or more Systems for a particular purpose. Deployment may be done on a Platform.
    DigitalCamera: URIRef  # The model as defined by the manufacturer.
    Dimension: URIRef  # The dimension of a 2D square or rectangular feature. Example, the dimension of a rectangular plot [Site](#EcologicalSite). This class should perhaps have specialised classes to express not just square or rectangular features but also others such as circular features.
    Distribution: URIRef  # A specific representation of a dataset. A dataset might be available in multiple serializations that may differ in various ways, including natural language, media-type or format, schematic organization, temporal and spatial resolution, level of detail or profiles (which might specify any or all of the above).
    EarthObservationSatellite: URIRef  # Earth observation satellites are satellites specifically designed to observe Earth from orbit, similar to spy satellites but intended for non-military uses such as environmental monitoring, meteorology, map making etc. Source: Wikipedia, http://en.wikipedia.org/wiki/Earth_observation_satellite Group: Platform_Details Entry_ID: Earth Observation Satellites Group: Platform_Identification Platform_Category: Earth Observation Satellites Short_Name: Earth Observation Satellites End_Group End_Group
    EcosystemProcessesSite: URIRef  # An ecological [Site](#EcologicalSite) that usually hosts a [FluxTower](#FluxTower).
    FeatureOfInterest: URIRef  # The thing whose property is being estimated or calculated in the course of an Observation to arrive at a Result or whose property is being manipulated by an Actuator, or which is being sampled or transformed in an act of Sampling.
    FixedPlatform: URIRef  # A fixed platform based on land.
    Float: URIRef  # Data type: Floating number.
    FluxTower: URIRef  # Across the globe, towers stand among the landscape, with sensors monitoring these eddies for carbon dioxide, water vapor and other gasses.  These so-called flux towers collect data on carbon dioxide exchange rates between the earth and atmosphere.
    IRI: URIRef  # None
    Input: URIRef  # *Input* - Any information that is provided to a [Procedure](#Procedure) for its use.
    Integer: URIRef  # Data type: Integer.
    ManagedFeature: URIRef  # None
    MaterialSample: URIRef  # A physical result of a sampling (or subsampling) event. In biological collections, the material sample is typically collected, and either preserved or destructively processed.
    Method: URIRef  # A Method describes in detailed steps how a workflow, protocol, plan or algorithm is carried out to make an [Observation](#Observation) or a [Sample](#Sample). It explains the steps to be carried out to arrive at reproducible [Result](#Result).
    MobilePlatform: URIRef  # A moving mobile platform on land, in water or in space.
    ObservableProperty: URIRef  # An observable quality (property, characteristic) of a [FeatureOfInterest](http://w3.org/ns/sosa/FeatureOfInterest). A feature-of-interest refers to a feature whose properties are measured or observed. 
    Observation: URIRef  # Act of carrying out an (Observation) [Procedure](#Procedure) to estimate or calculate a value of a property of a [FeatureOfInterest](http://w3.org/ns/sosa/FeatureOfInterest). Links to a [Sensor](http://w3.org/ns/sosa/Sensor) to describe what made the [Observation](#Observation) and how; links to an [ObservableProperty](#ObservableProperty) to describe what the result is an estimate of, and to a [FeatureOfInterest](http://w3.org/ns/sosa/FeatureOfInterest) to detail what that property was associated with.
    ObservationCollection: URIRef  # Collection of one or more observations, whose members share a common value for one or more property
    Parameter: URIRef  # A [FeatureOfInterest's](http://w3.org/ns/sosa/FeatureOfInterest) property or characteristic which an [Observation](#Observation) is measuring using some [Procedure](#Procedure).
    Platform: URIRef  # An entity that hosts other entities, particularly [Sensors](#Sensor), [Samplers](#Sampler), and other [Platforms](#Platform).
    Procedure: URIRef  # A workflow, protocol, plan, algorithm, or computational method specifying how to make an [Observation](#Observation), create a [Sample](#Sample), or make a change to the state of the world (via an [Actuator](http://w3.org/ns/sosa/Actuator). A [Procedure](#Procedure) is re-usable, and might be involved in many [Observations](#Observation), [Samplings](#Sampling), or [Actuations](http://w3.org/ns/sosa/Actuation). it explains the steps to be carried out to arrive at reproducible [Results](#Result).
    Quadrat: URIRef  # None
    RDFDataset: URIRef  # None
    Result: URIRef  # The result of an [Observation](https://w3id.org/tern/ontologies/tern/Observation), [Actuation](http://w3.org/ns/sosa/Actuation), or act of [Sampling](https://w3id.org/tern/ontologies/tern/Sampling).
    Sample: URIRef  # *A feature which is intended to be representative of a [FeatureOfInterest](http://w3.org/ns/sosa/FeatureOfInterest) on which [Observations](#Observation) may be made. Physical samples are sometimes known as physical specimens.
    Sampler: URIRef  # Sampler - A device that is used by, or implements, a (Sampling) [Procedure](#Procedure) to create or transform one or more samples. 
    Sampling: URIRef  # An activity of [Sampling](#Sampling) carries out a (Sampling) [Procedure](#Procedure) to create or transform one or more [Samples](#Sample).
    Sensor: URIRef  # Device, agent (including humans), or software (simulation) involved in, or implementing, a Procedure. Sensors respond to a stimulus, e.g., a change in the environment, or input data composed from the results of prior Observations, and generate a Result. Sensors can be hosted by Platforms.
    Site: URIRef  # An ecological monitoring site where where observations and samplings occur. This Site class is a subclass of [Sample](#Sample) since ecological sites are designed to be representative of an environmental system (which may be an ecosystem or bioregion) or zone (which may be a zone such as a parcel or tract).
    SiteVisit: URIRef  # A Site Visit is a discrete time-bounded activity at a [Site](#Site), during which [Sampling](#Sampling) or [Observation](#Observation) activities occur. 
    System: URIRef  # None
    Taxon: URIRef  # A group of organisms (sensu http://purl.obolibrary.org/obo/OBI_0100026) considered by taxonomists to form a homogeneous unit.
    Text: URIRef  # Class to encapsulate a textual value.
    Transect: URIRef  # None
    Value: URIRef  # A value of an [Attribute](https://w3id.org/tern/ontologies/tern/Attribute) or an [Observation](https://w3id.org/tern/ontologies/tern/Observation). 
    area: URIRef  # The extent of a [Site](#EcologicalSite) area, e.g., in m2
    attribute: URIRef  # Point to a concept representing the attribute.
    cardinalDirection: URIRef  # The cardinal direction of the *thing* represented as a string and expressed by cardinal and intercardinal points. 
    centroidPoint: URIRef  # The centroid point of an object-of-interest.
    dateCommissioned: URIRef  # The date when, e.g., a [Site](#EcologicalSite) is ready to commence its operations, after it is successfully installed and tested.
    dateDecommissioned: URIRef  # The date when, e.g., a [Site](#EcologicalSite) is decommissioned or stopped operating.
    dimension: URIRef  # Dimenion in metres.
    domain: URIRef  # The domain of the observation.
    equipment: URIRef  # Describe the equipment used as text.
    featureType: URIRef  # The feature type of a [Feature of Interest](#FeatureofInterest).
    fluxnetID: URIRef  # The unique identifier for flux towers registered with FLUXNET.
    globalMatch: URIRef  # Link a concept to an upper concept (in the closed system).
    globalValue: URIRef  # A property that links a concept from a vocabulary to another concept in an authoritative/endorsed vocabulary.
    globalVocabulary: URIRef  # The global vocabulary refers to the main vocabulary, which takes precedence over other similar vocabularies to promote data harmonisation.
    hasAttribute: URIRef  # Link to an [Attribute](#Attribute).
    hasCategoricalCollection: URIRef  # A property that links a concept to a collection containing its categorical values.
    hasEnvironmentalCharacteristic: URIRef  # The subject has some environmental characteristic. Points to a set of [Observations](#Observation) within an [EnvironmentalCharacteristic](#EnvironmentalCharacteristic).
    hasFeatureType: URIRef  # Links a concept to a feature type.
    hasMethod: URIRef  # A property that links a concept to a method.
    hasObservation: URIRef  # Link to an [Observation](#Observation).
    hasObservationTheme: URIRef  # Link a concept to an observation theme.
    hasParameter: URIRef  # A property that links a concept to a parameter.
    hasSampling: URIRef  # Link to a [Sampling](#Sampling) instance.
    hasSamplingPoint: URIRef  # A property that links, e.g., a [Sampling](#Sampling) to a [SamplingPoint](#SamplingPoint).
    hasSimpleValue: URIRef  # The direct link to the value either as an IRI or an RDF literal. The simple value is always equivalent to the value captured in [rdf:value](http://www.w3.org/1999/02/22-rdf-syntax-ns#value) of the tern:Value instance.
    hasSite: URIRef  # A property that links, e.g., a [SiteVisit](#EcologicalSiteVisit) to a [Site](#EcologicalSite).
    hasSiteVisit: URIRef  # A property that links, e.g., a [Site](#EcologicalSite) to a [Site Visit](#EcologicalSiteVisit).
    hasSubActivity: URIRef  # Link to an [Observation](#Observation) or [Sampling](#Sampling).
    hasValue: URIRef  # A link to a [tern:Value](https://w3id.org/tern/ontologies/tern/Value) which encapulates the value of this thing.
    instructions: URIRef  # Describe the instructions of the procedure/method.
    instrumentType: URIRef  # The type of instrument used.
    isAttributeOf: URIRef  # Link from an [Attribute](https://w3id.org/tern/ontologies/tern/Attribute) to some individual.
    isGlobalMatchOf: URIRef  # An inverse property of [globalMatch](#globalMatch); Links an upper concept to a concept (in the closed system).
    isSamplingPointOf: URIRef  # The inverse property [hasSamplingPoint](#hasSamplingPoint).
    isSiteOf: URIRef  # None
    isSiteVisitOf: URIRef  # None
    isSubActivityOf: URIRef  # A property that links an activity to its parent activity.
    length: URIRef  # A measure of distance.
    localValue: URIRef  # None
    localVocabulary: URIRef  # None
    locationDescription: URIRef  # The description of the location.
    locationProcedure: URIRef  # Link to a procedure used to obtain the location.
    methodType: URIRef  # A particular method type used to conduct some survey.
    observationType: URIRef  # The type of observation.
    purpose: URIRef  # Describe the purpose of something.
    resultDateTime: URIRef  # The result time is the instant of time when the Observation, Actuation or Sampling activity was completed.
    sampleStorageLocation: URIRef  # A property that links a [PhysicalSpecimen](#PhysicalSpecimen) to the location [Point](http://www.opengis.net/ont/sf#Point) of where it is stored.
    samplingType: URIRef  # The type of sampling act.
    scope: URIRef  # Describe the scope of something.
    shortName: URIRef  # None
    siteDescription: URIRef  # Contextual information is collected at each site. This includes measures of slope an aspect, surface strew and lithology, and information on the grazing and fire history of the site (Credit: TERN AusPlots).
    soilClassification: URIRef  # The term used to classify the SoilProfile.
    soilHorizonClassifier: URIRef  # Soil horizon classifier as defined in the Australian Soil and Land Survey Field Handbook on page 148.
    stratum: URIRef  # A stratum is a distinct, easily seen, layer of foliage and branches of a measurable height.
    swPoint: URIRef  # The south-west point of the subject.
    systemType: URIRef  # The type of system. Values are from some controlled vocabulary.
    taxon: URIRef  # Taxon classification.
    transectDirection: URIRef  # Describes the direction of the transect.
    transectEndPoint: URIRef  # Refers to the [sf:Point](http://www.opengis.net/ont/sf#Point) representing the end of a transect.
    transectStartPoint: URIRef  # Refers to the [sf:Point](http://www.opengis.net/ont/sf#Point) representing the start of a transect.
    uncertainty: URIRef  # Uncertainty for a quantitative value.
    unit: URIRef  # The unit of measure of the value. Use [QUDT units of measure vocabulary](http://qudt.org/vocab/unit/).
    valueType: URIRef  # Relates a Property to a specialisation of tern:Value.
    vocabulary: URIRef  # Controlled vocabulary, taxonomy etc.
    width: URIRef  # The measurement or extent of something from side to side.
