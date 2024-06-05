# GEMMA (GEneric Multilevel Modeling Abstraction)

GEMMA is a general purpose metamodel for moìultilevel modeling and simulation, designed to be adaptable to any modeling framework where multiple components interact. The objective is to support developers during the design phase of a multilevel simulator by providing a systematic approach for structuring multilevel systems and describing interactions between sub-models.
GEMMA is composed of the following elements:

- **M** is the set of atomic models
    
- **T** is the top-level component, which acts as the interface for the user, and provides a starting point for execution.
    
- **S** describes how levels are structured. It can be represented as a rooted tree, where the root is **T**, and the other nodes are elements of **M**. Each node is responsible for coordinating the execution of its descendants, if any. 
    
- **P** is the set of parameters of the model.
    
- **C**is the set of conditions that are used by a component to call an underlying component.
    
- **I** is the set of inputs to provide when a model is called.
    
- **O** is the set of outputs of the called model.
    
- **L** is the set of policies to maintain consistency. 
    
- **R** is the set of outputs of the model.

## Use cases
Two simple illustrative use cases are presented to prove the feasability of GEMMA
 - A pollution model where different types of vehicles emit local pollution within the considered environment
 . A smart territory model where vehicles act as data mule to carry sensor data in areas without Internet connection
