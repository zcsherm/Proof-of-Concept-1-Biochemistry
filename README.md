# Proof-of-Concept-1-Biochemistry
Testing and analysis of proposed system for organs and chemicals. 

## Description

This repository contains a crude prototype of an organism, it's genome, the simulations decoding schema, and the environment. Testing will be performed across several stages to determine this paradigms viability.

## Introduction

Our group is in the planning and requirement stages of building an artificial life simulator. One module that was proposed was to simulate organs and chemicals inside of the organism. As part of our planning, we constructed a simple prototype that tests this system across 3 areas, each of which should answer question about this paradigm:
* Stage 1:  
   * Can the decoding schema construct sufficient complexity with Genome string of acceptable length?
* Stage 2:  
  * How significant are mutations?
* Stage 3:
  * Can this system produce a functional organism?  

### Background

When it comes to artificial life, there is no real set method for designing a simulation. Instead, the system is determined by the use and purpose. Our aim is to create an ecosystem of multiple organisms and our purpose is to analyze how evolution affects the phase-state of the system.
In other words, how do organisms evolve in response to the evolution of other organisms. 

An issue arises from the scope of this project: There needs to be significant amount of freedom in the system to view the results we want. For example, if our simulation focused on a single animal with a fixed body plan, we coud standardize actions and chemical reactions across all instances. However, doing so with many agents of varying species can become very limiting. We wanted something that would allow each creature to slowly specialize in a way that wasn't hardcoded. A possible solution is to have the genome decode into organs and genes. Each organ would be a container for various bodily 'glands' and functions. Each gene describes some action that takes place in this organ, and each organ would activate each of these on each time step. This would allow for organs to develop in response to the environment and in truly emergent ways. It would also allow for groups of organs to develop a complex framework through which they interact. 

Rather than hardcoding behaviors, each organism would need to adapt and evolve the necessary responses to have a behavior. For example, we could hardcode that a mouse should run away from a cat. However, that's pretty limiting since this behaviour is not always a given. Mice that become infected with Toxoplasmosis actually lose this instinct and can become attracted to cats. Hardcoding can also reduce the variety of symbiotic relationships and other phenomena.

To solve this, we want our organisms to develop organs that react to certain stimuli and to release chemicals in response. The balance of these chemicals should drive behavior. Consider the fight or flight response: A human looks at something and if they perceive it as dangerous, their body preps them for responding in a way that is advantageous to survival. Looking below the surface we can see how we want our system to work. The sensory organ detects a stimulus (sight, smell, touch), and signals what was detected (quite possibly requiring the brain to decode the stilumus first). This signal causes catecholamines (in our simulation it could be any chemical) to be released into the blood stream. These chemicals trigger changes in the other organs and behavior is guided by how the chemical makeup of the body is rapidly changing. 

# Testing

## Stage 1

Before diving into complex testing, it is imperative that our system is functional. This stage will involve unit testing of various components and analyzing the results. 

#### Viability

The first part of the test aims to validate that a genome can actually be decoded into a creature and that the components and connections actually work. By performing this test on a large number of random genomes, we can also examine whether the paradigm produces a sufficiently variety of organisms and organs, or whether the system is attracted towards specific configurations.

After these tests, we construct an organism with a specific setup, and examine if chemical adjustments produce expected results. After, we can generate random genomes and measure their responses to chemical changes.

Finally, we plan to generate genomes of varying length and analyzing the number of structures that were decoded from the genome. This should paint a clearer picture of how long of a genome is needed to produce a sufficiently complex organism. We are hopeful that each organ may have dozens of genes, many of which may not ever be expressed.

## Stage 2

A major concern with this approach was centered on mutations. We feared that a mutation may cause too large of a change (for example, a mutation that causes a stop coding command to appear in the middle of an organ, could shift the reading frame for the rest of the organism). The phase should examine how impactful mutation is at varying rates, and methods.

#### Mutation Effect

The first part of the test involves producing a large number of offspring from a single genome, and measuring the difference between these offspring and the parent genome. We are hoping to see that similarity is high, with most mutations occuring on non-coding sections, some on parameters of a structure, and very few having a significant deleterious or transformative effect. This focuses on the entire genome.

The second part of testing focuses on the effect of mutation on specific organs and genes. We want to understand how strong mutation is on the phenotype produced by the structure. We hope to see mutations directly impacting the wiring and logic of these components. We're hopeful that we can quantify the percentage of mutations which impact coding vs non coding sections.

The third part focuses on cumulative effect of mutation. Given a particular genome, we want to iterate through a large number of generations, each time selecting an offspring at random. After a large number of generations, we can compare the difference between the source genome and the final genome.

The final part of this phase focuses on breeding populations. We plan to take 20 copies of a single genome and produce many offspring with random pairs of parents. Then 20 offspring are chosen to reproduce, and this is repeated for many generations. This should help us understand cross-over mutations that occur during reproduction, as well as the overall genetic drift the system allows and affords.

## Stage 3

The final stage of testing aims to see if random genomes can actually produce a creature that is capable of surviving in a simulation.

#### Genetic Search

This test is focused on using the creature structure in a genetic search algorithm to find an optimal survival chance. We've constructed a simple 2D environment that populates cells with food. A large number of random genomes are created and dropped into the grid. From this large population, we can take the organisms that were able to survive the longest and produce a subsequent generation. This is to be repeated a number of times and the metrics on the fitness function can be analyzed. We hope to see a continual improvement in fitness among generations. Repeating this several times should show considerable differentiation between successful genomes. Additionally, we may also see some cracks start to show, as organisms take advantage of mistakes in implementation, such as an organism discovering how to become biologically immortal or how to violate the laws of thermodynamics.
