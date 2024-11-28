# Brian2 Documentation

Brian is a simulator for spiking neural networks. It is written in the Python programming language and is available on almost all platforms. We believe that a simulator should not only save the time of processors, but also the time of scientists. Brian is therefore designed to be easy to learn and use, highly flexible and easily extensible.

To get an idea of what writing a simulation in Brian looks like, take a look at [a simple example](examples/CUBA.html), or run our [interactive demo](http://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=demo.ipynb).

You can actually edit and run the examples in the browser without having to install Brian, using the Binder service (note: sometimes this service is down or running slowly):

[![http://mybinder.org/badge.svg](http://mybinder.org/badge.svg)](http://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=demo.ipynb)

Once you have a feel for what is involved in using Brian, we recommend you start by following the [installation instructions](introduction/install.html), and in case you are new to the Python programming language, having a look at [Running Brian scripts](introduction/scripts.html). Then, go through the [tutorials](resources/tutorials/index.html), and finally read the [User Guide](user/index.html).

While reading the documentation, you will see the names of certain functions and classes are highlighted links (e.g. [`PoissonGroup`](reference/brian2.input.poissongroup.PoissonGroup.html#brian2.input.poissongroup.PoissonGroup "brian2.input.poissongroup.PoissonGroup")). Clicking on these will take you to the “reference documentation”. This section is automatically generated from the code, and includes complete and very detailed information, so for new users we recommend sticking to the [User’s guide](user/index.html). However, there is one feature that may be useful for all users. If you click on, for example, [`PoissonGroup`](reference/brian2.input.poissongroup.PoissonGroup.html#brian2.input.poissongroup.PoissonGroup "brian2.input.poissongroup.PoissonGroup"), and scroll down to the bottom, you’ll get a list of all the example code that uses [`PoissonGroup`](reference/brian2.input.poissongroup.PoissonGroup.html#brian2.input.poissongroup.PoissonGroup "brian2.input.poissongroup.PoissonGroup"). This is available for each class or method, and can be helpful in understanding how a feature works.

Finally, if you’re having problems, please do let us know at our [support page](introduction/support.html).

Please note that all interactions (e.g. via the mailing list or on github) should adhere to our [Code of Conduct](introduction/code_of_conduct.html).

---

# Adding support for new functions2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/developer/functions.html

# Adding support for new functions

For a description of Brian’s function system from the user point of view, see [Functions](../advanced/functions.html).

The default functions available in Brian are stored in the `DEFAULT_FUNCTIONS` dictionary. New [`Function`](../reference/brian2.core.functions.Function.html#brian2.core.functions.Function "brian2.core.functions.Function") objects can be added to this dictionary to make them available to all Brian code, independent of its namespace.

To add a new implementation for a code generation target, a `FunctionImplementation` can be added to the [`Function.implementations`](../reference/brian2.core.functions.Function.html#brian2.core.functions.Function.implementations "brian2.core.functions.Function.implementations") dictionary. The key for this dictionary has to be either a `CodeGenerator` class object, or a `CodeObject` class object. The `CodeGenerator` of a `CodeObject` (e.g. `CPPCodeGenerator` for `CPPStandaloneCodeObject`) is used as a fallback if no implementation specific to the `CodeObject` class exists.

If a function is already provided for the target language (e.g. it is part of a library imported by default), using the same name, all that is needed is to add an empty `FunctionImplementation` object to mark the function as implemented. For example, `exp` is a standard function in C++:
    
    
    DEFAULT_FUNCTIONS['exp'].implementations[CPPCodeGenerator] = FunctionImplementation()
    

Some functions are implemented but have a different name in the target language. In this case, the `FunctionImplementation` object only has to specify the new name:
    
    
    DEFAULT_FUNCTIONS['arcsin'].implementations[CPPCodeGenerator] = FunctionImplementation('asin')
    

Finally, the function might not exist in the target language at all, in this case the code for the function has to be provided, the exact form of this code is language-specific. In the case of C++, it’s a dictionary of code blocks:
    
    
    clip_code = {'support_code': '''
            double _clip(const float value, const float a_min, const float a_max)
            {
                    if (value < a_min)
                        return a_min;
                    if (value > a_max)
                        return a_max;
                    return value;
            }
            '''}
    DEFAULT_FUNCTIONS['clip'].implementations[CPPCodeGenerator] = FunctionImplementation('_clip',
                                                                                    code=clip_code)
    

---

# Advanced guide2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/advanced/index.html

# Advanced guide

This section has additional information on details not covered in the [User’s guide](../user/index.html).

  * [Functions](functions.html)
    * [Default functions](functions.html#default-functions)
    * [User-provided functions](functions.html#user-provided-functions)
  * [Preferences](preferences.html)
    * [Accessing and setting preferences](preferences.html#accessing-and-setting-preferences)
    * [Preference files](preferences.html#preference-files)
    * [List of preferences](preferences.html#list-of-preferences)
  * [Logging](logging.html)
    * [Logging and multiprocessing](logging.html#logging-and-multiprocessing)
    * [Showing/hiding log messages](logging.html#showing-hiding-log-messages)
    * [Preferences](logging.html#preferences)
  * [Namespaces](namespaces.html)
  * [Custom progress reporting](scheduling.html)
    * [Progress reporting](scheduling.html#progress-reporting)
  * [Random numbers](random.html)
    * [Seeding and reproducibility](random.html#seeding-and-reproducibility)
  * [Custom events](custom_events.html)
    * [Overview](custom_events.html#overview)
    * [Details](custom_events.html#details)
  * [State update](state_update.html)
    * [Explicit state update](state_update.html#explicit-state-update)
    * [Choice of state updaters](state_update.html#choice-of-state-updaters)
    * [Implicit state updates](state_update.html#implicit-state-updates)
  * [How Brian works](how_brian_works.html)
    * [Clock-driven versus event-driven](how_brian_works.html#clock-driven-versus-event-driven)
    * [Code overview](how_brian_works.html#code-overview)
    * [Syntax layer](how_brian_works.html#syntax-layer)
    * [Computational engine](how_brian_works.html#computational-engine)
  * [Interfacing with external code](interface.html)


---

# Changes for Brian 1 users2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/introduction/changes.html

# Changes for Brian 1 users

  * Physical units

  * Unported packages

  * Replacement packages

  * Removed classes/functions and their replacements

Note

If you need to run existing Brian 1 simulations, have a look at [Container image for Brian 1](brian1_to_2/container.html).

In most cases, Brian 2 works in a very similar way to Brian 1 but there are some important differences to be aware of. The major distinction is that in Brian 2 you need to be more explicit about the definition of your simulation in order to avoid inadvertent errors. In some cases, you will now get a warning in other even an error – often the error/warning message describes a way to resolve the issue.

Specific examples how to convert code from Brian 1 can be found in the document [Detailed Brian 1 to Brian 2 conversion notes](brian1_to_2/index.html).

## Physical units

The unit system now extends to arrays, e.g. `np.arange(5) * mV` will retain the units of volts and not discard them as Brian 1 did. Brian 2 is therefore also more strict in checking the units. For example, if the state variable `v` uses the unit of volt, the statement `G.v = np.rand(len(G)) / 1000.` will now raise an error. For consistency, units are returned everywhere, e.g. in monitors. If `mon` records a state variable v, `mon.t` will return a time in seconds and `mon.v` the stored values of `v` in units of volts.

If you need a pure numpy array without units for further processing, there are several options: if it is a state variable or a recorded variable in a monitor, appending an underscore will refer to the variable values without units, e.g. `mon.t_` returns pure floating point values. Alternatively, you can remove units by diving by the unit (e.g. `mon.t / second`) or by explicitly converting it (`np.asarray(mon.t)`).

Here’s an overview showing a few expressions and their respective values in Brian 1 and Brian 2:

Expression | Brian 1 | Brian 2  
---|---|---  
1 * mV | 1.0 * mvolt | 1.0 * mvolt  
np.array(1) * mV | 0.001 | 1.0 * mvolt  
np.array([1]) * mV | array([ 0.001]) | array([1.]) * mvolt  
np.mean(np.arange(5) * mV) | 0.002 | 2.0 * mvolt  
np.arange(2) * mV | array([ 0. , 0.001]) | array([ 0., 1.]) * mvolt  
(np.arange(2) * mV) >= 1 * mV | array([False, True], dtype=bool) | array([False, True], dtype=bool)  
(np.arange(2) * mV)[0] >= 1 * mV | False | False  
(np.arange(2) * mV)[1] >= 1 * mV | DimensionMismatchError | True  
  

---

# Code generation2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/developer/codegen.html

# Code generation  
  
The generation of a code snippet is done by a `CodeGenerator` class. The templates are stored in the `CodeObject.templater` attribute, which is typically implemented as a subdirectory of templates. The compilation and running of code is done by a `CodeObject`. See the sections below for each of these.

## Code path

The following gives an outline of the key steps that happen for the code generation associated to a [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") `StateUpdater`. The items in grey are Brian core functions and methods and do not need to be implemented to create a new code generation target or device. The parts in yellow are used when creating a new device. The parts in green relate to generating code snippets from abstract code blocks. The parts in blue relate to creating new templates which these snippets are inserted into. The parts in red relate to creating new runtime behaviour (compiling and running generated code).

![../_images/codegen_code_paths.png](../_images/codegen_code_paths.png)

In brief, what happens can be summarised as follows. [`Network.run`](../reference/brian2.core.network.Network.html#brian2.core.network.Network.run "brian2.core.network.Network.run") will call [`BrianObject.before_run`](../reference/brian2.core.base.BrianObject.html#brian2.core.base.BrianObject.before_run "brian2.core.base.BrianObject.before_run") on each of the objects in the network. Objects such as `StateUpdater`, which is a subclass of [`CodeRunner`](../reference/brian2.groups.group.CodeRunner.html#brian2.groups.group.CodeRunner "brian2.groups.group.CodeRunner") use this spot to generate and compile their code. The process for doing this is to first create the abstract code block, done in the `StateUpdater.update_abstract_code` method. Then, a `CodeObject` is created with this code block. In doing so, Brian will call out to the currently active `Device` to get the `CodeObject` and `CodeGenerator` classes associated to the device, and this hierarchy of calls gives several hooks which can be changed to implement new targets.

## Code generation

To implement a new language, or variant of an existing language, derive a class from `CodeGenerator`. Good examples to look at are the `NumpyCodeGenerator`, `CPPCodeGenerator` and `CythonCodeGenerator` classes in the `brian2.codegen.generators` package. Each `CodeGenerator` has a `class_name` attribute which is a string used by the user to refer to this code generator (for example, when defining function implementations).

The derived `CodeGenerator` class should implement the methods marked as `NotImplemented` in the base `CodeGenerator` class. `CodeGenerator` also has several handy utility methods to make it easier to write these, see the existing examples to get an idea of how these work.

## Syntax translation

One aspect of writing a new language is that sometimes you need to translate from Python syntax into the syntax of another language. You are free to do this however you like, but we recommend using a `NodeRenderer` class which allows you to iterate over the abstract syntax tree of an expression. See examples in `brian2.parsing.rendering`.

## Templates

In addition to snippet generation, you need to create templates for the new language. See the `templates` directories in `brian2.codegen.runtime.*` for examples of these. They are written in the Jinja2 templating system. The location of these templates is set as the `CodeObject.templater` attribute. Examples such as `CPPCodeObject` show how this is done.

### Template structure

Languages typically define a `common_group` template that is the base for all other templates. This template sets up the basic code structure that will be reused by all code objects, e.g. by defining a function header and body, and adding standard imports/includes. This template defines several blocks, in particular a `maincode` clock containing the actual code that is specific to each code object. The specific templates such as `reset` then derive from the `common_group` base template and override the `maincode` block. The base template can also define additional blocks that are sometimes but not always overwritten. For example, the `common_group.cpp` template of the C++ standalone code generator defines an `extra_headers` block that can be overwritten by child templates to include additional header files needed for the code in `maincode`.

### Template keywords

Templates also specify additional information necessary for the code generation process as Jinja comments (`{# ... #}`). The following keywords are recognized by Brian:

`USES_VARIABLES`
    

Lists variable names that are used by the template, even if they are not referred to in user code.

`WRITES_TO_READ_ONLY_VARIABLES`
    

Lists read-only variables that are modified by the template. Normally, read-only variables are not considered to change during code execution, but e.g. synapse creation requires changes to synaptic indices that are considered read-only otherwise.

`ALLOWS_SCALAR_WRITE`
    

The presence of this keyword means that in this template, writing to scalar variables is permitted. Writing to scalar variables is not permitted by default, because it can be ambiguous in contexts that do not involve all neurons/synapses. For example, should the statement `scalar_variable += 1` in a reset statement update the variable once or once for every spiking neuron?

`ITERATE_ALL`
    

Lists indices that are iterated over completely. For example, during the state update or threshold step, the template iterates over all neurons with the standard index `_idx`. When executing the reset statements on the other hand, not all neurons are concerned. This is only used for the numpy code generation target, where it allows avoiding expensive unnecessary indexing.

## Code objects

To allow the final code block to be compiled and run, derive a class from `CodeObject`. This class should implement the placeholder methods defined in the base class. The class should also have attributes `templater` (which should be a `Templater` object pointing to the directory where the templates are stored) `generator_class` (which should be the `CodeGenerator` class), and `class_name` (which should be a string the user can use to refer to this code generation target.

## Default functions

You will typically want to implement the default functions such as the trigonometric, exponential and `rand` functions. We usually put these implementations either in the same module as the `CodeGenerator` class or the `CodeObject` class depending on whether they are language-specific or runtime target specific. See those modules for examples of implementing these functions.

## Code guide

  * `brian2.codegen`: everything related to code generation

  * `brian2.codegen.generators`: snippet generation, including the `CodeGenerator` classes and default function implementations.

  * `brian2.codegen.runtime`: templates, compilation and running of code, including `CodeObject` and default function implementations.

  * `brian2.core.functions`, `brian2.core.variables`: these define the values that variable names can have.

  * `brian2.parsing`: tools for parsing expressions, etc.

  * `brian2.parsing.rendering`: AST tools for rendering expressions in Python into different languages.

  * `brian2.utils`: various tools for string manipulation, file management, etc.

## Additional information

For some additional (older, but still accurate) notes on code generation:

  * [Older notes on code generation](oldcodegen.html)
    * [Stages of code generation](oldcodegen.html#stages-of-code-generation)
    * [Key concepts](oldcodegen.html#key-concepts)
    * [Code guide](oldcodegen.html#code-guide)

---

# Compatibility and reproducibility2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/introduction/compatibility.html

# Compatibility and reproducibility

## Supported Python and numpy versions

We follow the approach outlined in numpy’s [deprecation policy](https://numpy.org/neps/nep-0029-deprecation_policy.html). This means that Brian supports:

  * All minor versions of Python released 42 months prior to Brian, and at minimum the two latest minor versions.

  * All minor versions of numpy released in the 24 months prior to Brian, and at minimum the last three minor versions.

Note that we do not have control about the versions that are supported by the [conda-forge](https://conda-forge.org/) infrastructure. Therefore, `brian2` conda packages might not be provided for all of the supported versions. In this case, affected users can chose to either update the Python/numpy version in their conda environment to a version with a conda package or to install `brian2` via pip.

## General policy

We try to keep backwards-incompatible changes to a minimum. In general, `brian2` scripts should continue to work with newer versions and should give the same results.

As an exception to the above rule, we will always correct clearly identified bugs that lead to incorrect simulation results (i.e., not just an matter of interpretation). Since we do not want to require new users to take any action to get correct results, we will change the default behaviour in such cases. If possible, we will give the user an option to restore the old, incorrect behaviour to reproduce the previous results with newer Brian versions. This would typically be a preference in the `legacy` category, see [legacy.refractory_timing](../advanced/preferences.html#brian-pref-legacy-refractory-timing) for an example.

Note

The order of terms when evaluating equations is not fixed and can change with the version of `sympy`, the symbolic mathematics library used in Brian. Similarly, Brian performs a number of optimizations by default and asks the compiler to perform further ones which might introduce subtle changes depending on the compiler and its version. Finally, code generation can lead to either Python or C++ code (with a single or multiple threads) executing the actual simulation which again may affect the numerical results. Therefore, we cannot guarantee exact, “bitwise” reproducibility of results.

## Syntax deprecations

We sometimes realize that the names of arguments or other syntax elements are confusing and therefore decide to change them. In such cases, we start to use the new syntax everywhere in the documentation and examples, but leave the former syntax available for compatiblity with previously written code. For example, earlier versions of Brian used `method='linear'` to describe the exact solution of differential equations via sympy (that most importantly applies to “linear” equations, i.e. linear differential equations with constant coefficients). However, some users interpreted `method='linear'` as a “linear approximation” like the forward Euler method. In newer versions of Brian the recommended syntax is therefore to use `method='exact'`, but the old syntax remains valid.

If the changed syntax is very prominent, its continued use in Brian scripts (published by others) could be confusing to new users. In these cases, we might decide to give a warning when the deprecated syntax is used (e.g. for the `pre` and `post` arguments in [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses") which have been replaced by `on_pre` and `on_post`). Such warnings will contain all the information necessary to rewrite the code so that the warning is no longer raised (in line with our general [policy for warnings](../developer/guidelines/logging.html#log-level-recommendations)).

## Random numbers

Streams of random numbers in Brian simulations (including the generation of synapses, etc.) are reproducible when a seed is set via Brian’s [`seed()`](../reference/brian2.devices.device.seed.html#brian2.devices.device.seed "brian2.devices.device.seed") function. Note that there is a difference with regard to random numbers between [runtime and standalone mode](../user/computation.html): in runtime mode, numpy’s random number generator is always used – even from generated Cython code. Therefore, the call to [`seed()`](../reference/brian2.devices.device.seed.html#brian2.devices.device.seed "brian2.devices.device.seed") will set numpy’s random number generator seed which then applies to all random numbers. Regardless of whether initial values of a variable are set via an explicit call to [`numpy.random.randn`](https://numpy.org/doc/stable/reference/random/generated/numpy.random.randn.html#numpy.random.randn "\(in NumPy v2.0\)"), or via a Brian expression such as `'randn()'`, both are affected by this seed. In contrast, random numbers in standalone simulations will be generated by an independent random number generator (but based on the same algorithm as numpy’s) and the call to [`seed()`](../reference/brian2.devices.device.seed.html#brian2.devices.device.seed "brian2.devices.device.seed") will only affect these numbers, not numbers resulting from explicit calls to [`numpy.random`](https://numpy.org/doc/stable/reference/random/index.html#module-numpy.random "\(in NumPy v2.0\)"). To make standalone scripts mixing both sources of randomness reproducible, either set numpy’s random generator seed manually in addition to calling [`seed()`](../reference/brian2.devices.device.seed.html#brian2.devices.device.seed "brian2.devices.device.seed"), or reformulate the model to use code generation everywhere (e.g. replace `group.v = -70*mV + 10*mV*np.random.randn(len(group))` by `group.v = '-70*mv + 10*mV*randn()'`).

Changing the code generation target can imply a change in the order in which random numbers are drawn from the reproducible random number stream. In general, we therefore only guarantee the use of the same numbers if the code generation target and the number of threads (for C++ standalone simulations) is the same.

Note

If there are several sources of randomness (e.g. multiple [`PoissonGroup`](../reference/brian2.input.poissongroup.PoissonGroup.html#brian2.input.poissongroup.PoissonGroup "brian2.input.poissongroup.PoissonGroup") objects) in a simulation, then the order in which these elements are executed matters. The order of execution is deterministic, but if it is not unambiguously determined by the `when` and `order` attributes (see [Scheduling](../user/running.html#scheduling) for details), then it will depend on the names of objects. When not explicitly given via the `name` argument during the object’s creation, names are automatically generated by Brian as e.g. `poissongroup`, `poissongroup_1`, etc. When you repeatedly run simulations within the same process, these names might change and therefore the order in which the elements are simulated. Random numbers will then be differently distributed to the objects. To avoid this and get reproducible random number streams you can either fix the order of elements by specifying the `order` or `name` argument, or make sure that each simulation gets run in a fresh Python process.

## Python errors

While we try to guarantee the reproducibility of simulations (within the limits stated above), we do so only for code that does not raise any error. We constantly try to improve the error handling in Brian, and these improvements can lead to errors raised at a different time (e.g. when creating an object as opposed to when running the simulation), different types of errors being raised (e.g. [`DimensionMismatchError`](../reference/brian2.units.fundamentalunits.DimensionMismatchError.html#brian2.units.fundamentalunits.DimensionMismatchError "brian2.units.fundamentalunits.DimensionMismatchError") instead of [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.12\)")), or simply a different error message text. Therefore, Brian scripts should never use `try`/`except` blocks to implement program logic.

---

# Computational methods and efficiency2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/user/computation.html

# Computational methods and efficiency

  * Runtime code generation

    * Caching

  * Standalone code generation

    * Single run call

    * Multiple run calls

    * Multiple full simulation runs

    * Limitations

    * Variables

    * Multi-threading with OpenMP

    * Custom code injection

    * Customizing the build process

    * Cleaning up after a run

  * Compiler settings

Brian has several different methods for running the computations in a simulation. The default mode is Runtime code generation, which runs the simulation loop in Python but compiles and executes the modules doing the actual simulation work (numerical integration, synaptic propagation, etc.) in a defined target language. Brian will select the best available target language automatically. On Windows, to ensure that you get the advantages of compiled code, read the instructions on installing a suitable compiler in [Requirements for C++ code generation](../introduction/install.html#installation-cpp). Runtime mode has the advantage that you can combine the computations performed by Brian with arbitrary Python code specified as [`NetworkOperation`](../reference/brian2.core.operations.NetworkOperation.html#brian2.core.operations.NetworkOperation "brian2.core.operations.NetworkOperation").

The fact that the simulation is run in Python means that there is a (potentially big) overhead for each simulated time step. An alternative is to run Brian in with Standalone code generation – this is in general faster (for certain types of simulations _much_ faster) but cannot be used for all kinds of simulations. To enable this mode, add the following line after your Brian import, but before your simulation code:
    
    
    set_device('cpp_standalone')
    

For detailed control over the compilation process (both for runtime and standalone code generation), you can change the Cleaning up after a run that are used.

The following topics are not essential for beginners.

  

## Runtime code generation

Code generation means that Brian takes the Python code and strings in your model and generates code in one of several possible different languages which is then executed. The target language for this code generation process is set in the [codegen.target](../reference/brian2.codegen.html#brian-pref-codegen-target) preference. By default, this preference is set to `'auto'`, meaning that it will choose the compiled language target if possible and fall back to Python otherwise (also raising a warning). The compiled language target is `'cython'` which needs the [Cython](http://cython.org/) package in addition to a working C++ compiler. If you want to chose a code generation target explicitly (e.g. because you want to get rid of the warning that only the Python fallback is available), set the preference to `'numpy'` or `'cython'` at the beginning of your script:
    
    
    from brian2 import *
    prefs.codegen.target = 'numpy'  # use the Python fallback
    

See [Preferences](../advanced/preferences.html) for different ways of setting preferences.

> ### Caching

When you run code with `cython` for the first time, it will take some time to compile the code. For short simulations, this can make these targets to appear slow compared to the `numpy` target where such compilation is not necessary. However, the compiled code is stored on disk and will be re-used for later runs, making these simulations start faster. If you run many simulations with different code (e.g. Brian’s [test suite](../developer/guidelines/testing.html)), this code can take quite a bit of space on the disk. During the import of the `brian2` package, we check whether the size of the disk cache exceeds the value set by the [codegen.max_cache_dir_size](../reference/brian2.codegen.html#brian-pref-codegen-max-cache-dir-size) preference (by default, 1GB) and display a message if this is the case. You can clear the disk cache manually, or use the [`clear_cache`](../reference/brian2.__init__.clear_cache.html#brian2.__init__.clear_cache "brian2.__init__.clear_cache") function, e.g. `clear_cache('cython')`.

Note

If you run simulations on parallel on a machine using the Network File System, see [this known issue](../introduction/known_issues.html#parallel-cython).

## Standalone code generation

Brian supports generating standalone code for multiple devices. In this mode, running a Brian script generates source code in a project tree for the target device/language. This code can then be compiled and run on the device, and modified if needed. At the moment, the only “device” supported is standalone C++ code. In some cases, the speed gains can be impressive, in particular for smaller networks with complicated spike propagation rules (such as STDP).

To use the C++ standalone mode, you only have to make very small changes to your script. The exact change depends on whether your script has only a single [`run()`](../reference/brian2.core.magic.run.html#brian2.core.magic.run "brian2.core.magic.run") (or [`Network.run`](../reference/brian2.core.network.Network.html#brian2.core.network.Network.run "brian2.core.network.Network.run")) call, or several of them:

### Single run call

At the beginning of the script, i.e. after the import statements, add:
    
    
    set_device('cpp_standalone')
    

The `Device.build` function will be automatically called with default arguments right after the [`run()`](../reference/brian2.core.magic.run.html#brian2.core.magic.run "brian2.core.magic.run") call. If you need non-standard arguments then you can specify them as part of the [`set_device()`](../reference/brian2.devices.device.set_device.html#brian2.devices.device.set_device "brian2.devices.device.set_device") call:
    
    
    set_device('cpp_standalone', directory='my_directory', debug=True)
    

### Multiple run calls

At the beginning of the script, i.e. after the import statements, add:
    
    
    set_device('cpp_standalone', build_on_run=False)
    

After the last [`run()`](../reference/brian2.core.magic.run.html#brian2.core.magic.run "brian2.core.magic.run") call, call `CPPStandaloneDevice.build` explicitly:
    
    
    device.build()
    

The `build` function has several arguments to specify the output directory, whether or not to compile and run the project after creating it and whether or not to compile it with debugging support or not.

### Multiple full simulation runs

To run multiple full, independent, simulations (i.e. not just multiple [`run()`](../reference/brian2.core.magic.run.html#brian2.core.magic.run "brian2.core.magic.run") calls as discussed above), you can use the device’s [`run`](../reference/brian2.devices.cpp_standalone.device.CPPStandaloneDevice.html#brian2.devices.cpp_standalone.device.CPPStandaloneDevice.run "brian2.devices.cpp_standalone.device.CPPStandaloneDevice.run") function after an initial build. This will use the previously generated and compiled code, and will therefore run immediately. Note that you cannot change the model or its parameters in the usual way between the [`build`](../reference/brian2.devices.cpp_standalone.device.CPPStandaloneDevice.html#brian2.devices.cpp_standalone.device.CPPStandaloneDevice.build "brian2.devices.cpp_standalone.device.CPPStandaloneDevice.build") and [`run`](../reference/brian2.devices.cpp_standalone.device.CPPStandaloneDevice.html#brian2.devices.cpp_standalone.device.CPPStandaloneDevice.run "brian2.devices.cpp_standalone.device.CPPStandaloneDevice.run") calls. If you want to change some of its parameters, you will have to use the `run_args` argument as described below.

#### Running multiple simulations with same parameters

By default, a device’s [`run`](../reference/brian2.devices.cpp_standalone.device.CPPStandaloneDevice.html#brian2.devices.cpp_standalone.device.CPPStandaloneDevice.run "brian2.devices.cpp_standalone.device.CPPStandaloneDevice.run") will run the simulation again, using the same model parameters and initializations. This can be useful, when the model is itself stochastic (e.g. using the `xi` noise term in the equations, using a stochastic group such as [`PoissonGroup`](../reference/brian2.input.poissongroup.PoissonGroup.html#brian2.input.poissongroup.PoissonGroup "brian2.input.poissongroup.PoissonGroup") or [`PoissonInput`](../reference/brian2.input.poissoninput.PoissonInput.html#brian2.input.poissoninput.PoissonInput "brian2.input.poissoninput.PoissonInput"), etc.), when it uses random synaptic connections, or when it uses random variable initialization:
    
    
    set_device('cpp_standalone')
    group = NeuronGroup(1, 'dv/dt = -v / (10*ms) : 1')  # a simple IF neuron without threshold
    group.v = 'rand()'  # v is randomly initialized between 0 and 1
    mon = StateMonitor(group, 'v', record=0)
    run(100*ms)  # calls device.build and device.run
    results = [mon.v[0]]
    # Do 9 more runs without recompiling, each time initializing v to a new value
    for _ in range(9):
        device.run()
        results.append(mon.v[0])
    

For more consistent code, you might consider to disable the automatic `device.build`/`device.run` call, so that the initial run of the simulation is not different to subsequent runs:
    
    
    set_device('cpp_standalone', build_on_run=False)
    # ... Set up model as before
    run(100*ms)  # will not call device.build/device.run
    device.build(run=False)  # Compile the code
    results = []
    # Do 10 runs without recompiling, each time initializing v to a new value
    for _ in range(10):
        device.run()
        results.append(mon.v[0])
    

#### Running multiple simulations with different parameters

When launching new simulation runs as described above, you can also change parameters of the model. Note that this only concerns parameters that are included in equations, you cannot change externally defined constants. You can easily work around this limitation, however, by declaring such constants in the equations, using the `(shared, constant)` flags. Here’s a similar example to the one shown before, now exploring the effect of the time constant `tau`, while assuring via a [`seed()`](../reference/brian2.devices.device.seed.html#brian2.devices.device.seed "brian2.devices.device.seed") call that the random initializations are identical across runs:
    
    
    set_device('cpp_standalone', build_on_run=False)
    seed(111)  # same random numbers for each run
    group = NeuronGroup(10, '''dv/dt = -v / tau : 1
                               tau : second (shared, constant)''')  # 10 simple IF neuron without threshold
    group.v = 'rand()'
    mon = StateMonitor(group, 'v', record=0)
    run(100*ms)
    device.build(run=False)  # Compile the code
    results = []
    # Do 10 runs without recompiling, each time setting group.tau to a new value
    for tau_value in (np.arange(10)+1)*5*ms:
        device.run(run_args={group.tau: tau_value})
        results.append(mon.v[:])
    

You can use the same mechanism to provide an array of initial values for a group. E.g., to systematically try out different initializations of `v`, you could use:
    
    
    set_device('cpp_standalone', build_on_run=False)
    group = NeuronGroup(10, 'dv/dt = -v / (10*ms) : 1')  # ten simple IF neurons without threshold
    mon = StateMonitor(group, 'v', record=True)
    run(100*ms)  # will not call device.build/device.run
    device.build(run=False)  # Compile the code
    results = []
    # Do 10 runs without recompiling, each time initializing v differently
    for idx in range(10):
        device.run(run_args={group.v: np.arange(10)*0.01 + 0.1*idx})
        results.append(mon.v[0])
    

You can also overwrite the values in a [`TimedArray`](../reference/brian2.input.timedarray.TimedArray.html#brian2.input.timedarray.TimedArray "brian2.input.timedarray.TimedArray") using this mechanism, by using the [`TimedArray`](../reference/brian2.input.timedarray.TimedArray.html#brian2.input.timedarray.TimedArray "brian2.input.timedarray.TimedArray") as a key in the `run_args` dictionary:
    
    
    set_device('cpp_standalone', build_on_run=False)
    stim = TimedArray(np.zeros(10), dt=10*ms)
    group = NeuronGroup(10, 'dv/dt = (stim(t) - v)/ (10*ms) : 1')  # time-dependent stimulus
    mon = StateMonitor(group, 'v', record=True)
    run(100 * ms)
    device.build(run=False)
    results = []
    # Do 10 runs with a 10ms at a random time
    for idx in range(10):
        values = np.zeros(10)
        values[np.random.randint(0, 10)] = 1
        device.run(run_args={stim: values})
        results.append(mon.v[0])
    

By default, the initialization provided via `run_args` overwrites any initializations done in the usual way. This might not exactly do what you want if you use string-based variable initializations that refer to each other. For example, if your equations contain two synaptic time constants `tau_exc` and `tau_inh`, and you always want the latter to be twice the value of the former, you can write:
    
    
    group.tau_exc = 5*ms
    group.tau_inh = 'tau_exc * 2'
    

If you now use the `run_args` argument to set `tau_exc` to a different value, this will not be taken into account for setting `tau_inh`, since the value change for `tau_exc` happens _after_ the initialization of `tau_inh`. Of course you can simply set the value for `tau_inh` manually using `run_args` as well, but a more general solution is to move the point where the `run_args` are applied. You can do this by calling the device’s [`apply_run_args`](../reference/brian2.devices.cpp_standalone.device.CPPStandaloneDevice.html#brian2.devices.cpp_standalone.device.CPPStandaloneDevice.apply_run_args "brian2.devices.cpp_standalone.device.CPPStandaloneDevice.apply_run_args") function:
    
    
    group.tau_exc = 5*ms
    device.apply_run_args()
    group.tau_inh = 'tau_exc * 2'
    

With this change, setting `tau_exc` via `run_args` will affect the value of `tau_inh`.

#### Running multiple simulations in parallel

The techniques mentioned above cannot be directly used to run simulations in parallel (e.g. with Python’s [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing "\(in Python v3.12\)") module), since all of them will try to write the results to the same place. You can circumvent this problem by specifying the `results_directory` argument, and setting it to a different value for each run. Note that using the standalone device with [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing "\(in Python v3.12\)") can be a bit tricky, since the currently selected device is stored globally in the `device` module. Use the approach presented below to make sure the device is selected correctly. Here’s a variant of the previously shown example running a simulation with random initialization repeatedly, this time running everything in parallel using Python’s [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing "\(in Python v3.12\)") module:
    
    
    class SimWrapper:
        def __init__(self):
            # Runs once to set up the simulation
            group = NeuronGroup(1, 'dv/dt = -v / (10*ms) : 1', name='group')
            group.v = 'rand()'  # v is randomly initialized between 0 and 1
            mon = StateMonitor(group, 'v', record=0, name='monitor')
            # Store everything in a network
            self.network = Network([group, mon])
            self.network.run(100*ms)
            device.build(run=False)
            self.device = get_device()  # store device object
    
        def do_run(self, result_dir):
            # Runs in every process
            # Workaround to set the device globally in this context
            from brian2.devices import device_module
            device_module.active_device = self.device
            self.device.run(results_directory=result_dir)
            # Return the results
            return self.network['monitor'].v[0]
    
    if __name__ == '__main__':  # Important for running on Windows and OS X
        set_device('cpp_standalone', build_on_run=False)
        sim = SimWrapper()
        import multiprocessing
        with multiprocessing.Pool() as p:
            # Run 10 simulations in parallel
            results = p.map(sim.do_run, [f'result_{idx}' for idx in range(10)])
    

You can also use parallel runs with the `run_args` argument. For example, to do 10 simulations with different (deterministic) initial values for `v`:
    
    
    class SimWrapper:
        # ... model definition without random initialization
    
        def do_run(self, v_init):
            # Set result directory based on variable
            result_dir = f'result_{v_init}'
            self.device.run(run_args={self.network['group'].v: v_init},
                            results_directory=result_dir)
            # Return the results
            return self.network['monitor'].v[0]
    
    if __name__ == '__main__':  # Important for running on Windows and OS X
        set_device('cpp_standalone', build_on_run=False)
        sim = SimWrapper()
        import multiprocessing
        with multiprocessing.Pool() as p:
            # Run 10 simulations in parallel
            results = p.map(sim.do_run, np.linspace(0, 1, 10))
    

Note

Python’s [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing "\(in Python v3.12\)") module cannot deal with user-defined functions (including [`TimedArray`](../reference/brian2.input.timedarray.TimedArray.html#brian2.input.timedarray.TimedArray "brian2.input.timedarray.TimedArray")) and other complex code structures. If you run into [`PicklingError`](https://docs.python.org/3/library/pickle.html#pickle.PicklingError "\(in Python v3.12\)") or [`AttributeError`](https://docs.python.org/3/library/exceptions.html#AttributeError "\(in Python v3.12\)") exceptions, you might have to use the `pathos` (<https://pypi.org/project/pathos>) package instead, which can handle more complex code structures.

### Limitations

Not all features of Brian will work with C++ standalone, in particular Python based network operations and some array based syntax such as `S.w[0, :] = ...` will not work. If possible, rewrite these using string based syntax and they should work. Also note that since the Python code actually runs as normal, code that does something like this may not behave as you would like:
    
    
    results = []
    for val in vals:
        # set up a network
        run()
        results.append(result)
    

The current C++ standalone code generation only works for a fixed number of `run` statements, not with loops. If you need to do loops or other features not supported automatically, you can do so by inspecting the generated C++ source code and modifying it, or by inserting code directly into the main loop as described below.

### Variables

In standalone mode, code will only be executed when the simulation is run (after the [`run()`](../reference/brian2.core.magic.run.html#brian2.core.magic.run "brian2.core.magic.run") call by default, or after a call to `build`, if [`set_device()`](../reference/brian2.devices.device.set_device.html#brian2.devices.device.set_device "brian2.devices.device.set_device") has been called with `build_on_run` set to `False`). This means that it is not possible to access state variables and synaptic connection indices in the Python script doing the set up of the model. For example, the following code would work fine in runtime mode, but raise a `NotImplementedError` in standalone mode:
    
    
    neuron = NeuronGroup(10, 'v : volt')
    neuron.v = '-70*mV + rand()*10*mV'
    print(np.mean(neuron.v))
    

Sometimes, access is needed to make one variable depend on another variable for initialization. In such cases, it is often possible to circumvent the issue by using initialization with string expressions for both variables. For example, to set the initial membrane potential relative to a random leak reversal potential, the following code would work in runtime mode but fail in standalone mode:
    
    
    neuron = NeuronGroup(10, 'dv/dt = -g_L*(v - E_L)/tau : volt')
    neuron.E_L = '-70*mV + rand()*10*mV'  # E_L between -70mV and -60mV
    neuron.v = neuron.E_L  # initial membrane potential equal to E_L
    

Instead, you can initialize the variable `v` with a string expression, which means that standalone will execute it during the run when the value of `E_L` is available:
    
    
    neuron = NeuronGroup(10, 'dv/dt = -g_L*(v - E_L)/tau : volt')
    neuron.E_L = '-70*mV + rand()*10*mV'  # E_L between -70mV and -60mV
    neuron.v = 'E_L'  # works both in runtime and standalone mode
    

The same applies to synaptic indices. For example, if we want to set weights differently depending on the target index of a synapse, the following would work in runtime mode but fail in standalone mode, since the synaptic indices have not been determined yet:
    
    
    neurons = NeuronGroup(10, '')
    synapses = Synapses(neurons, neurons, 'w : 1')
    synapses.connect(p=0.25)
    # Set weights to low values when targetting first five neurons and to high values otherwise
    synapses.w[:, :5] = 0.1
    synapses.w[:, 5:] = 0.9
    

Again, this initialization can be replaced by string expressions, so that standalone mode can evaluate them in the generated code after synapse creation:
    
    
    neurons = NeuronGroup(10, '')
    synapses = Synapses(neurons, neurons, 'w : 1')
    synapses.connect(p=0.25)
    # Set weights to low values when targetting first five neurons and to high values otherwise
    synapses.w['j < 5'] = 0.1
    synapses.w['j >= 5'] = 0.9
    

Note that this limitation only applies if the variables or synapses have been initialized in ways that require the execution of code. If instead they are initialized with concrete values, they can be accessed in Python code even in standalone mode:
    
    
    neurons = NeuronGroup(10, 'v : volt')
    neurons.v = -70*mV
    print(np.mean(neurons.v))  # works in standalone
    synapses = Synapses(neurons, neurons, 'w : 1')
    synapses.connect(i=[0, 2, 4, 6, 8], j=[1, 3, 5, 7, 9])
    # works as well, since synaptic indices are known
    synapses.w[:, :5] = 0.1
    synapses.w[:, 5:] = 0.9
    

In any case, state variables, synaptic indices, and monitored variables can be accessed using standard syntax _after_ a run (with a few exceptions, e.g. string expressions for indexing).

### Multi-threading with OpenMP

Warning

OpenMP code has not yet been well tested and so may be inaccurate.

When using the C++ standalone mode, you have the opportunity to turn on multi-threading, if your C++ compiler is compatible with OpenMP. By default, this option is turned off and only one thread is used. However, by changing the preferences of the codegen.cpp_standalone object, you can turn it on. To do so, just add the following line in your python script:
    
    
    prefs.devices.cpp_standalone.openmp_threads = XX
    

XX should be a positive value representing the number of threads that will be used during the simulation. Note that the speedup will strongly depend on the network, so there is no guarantee that the speedup will be linear as a function of the number of threads. However, this is working fine for networks with not too small timestep (dt > 0.1ms), and results do not depend on the number of threads used in the simulation.

### Custom code injection

It is possible to insert custom code directly into the generated code of a standalone simulation using a Device’s [`insert_code`](../reference/brian2.devices.device.Device.html#brian2.devices.device.Device.insert_code "brian2.devices.device.Device.insert_code") method:
    
    
    device.insert_code(slot, code)
    

`slot` can be one of `main`, `before_start`, `after_start`, `before_network_run`, `after_network_run`, `before_end` and `after_end`, which determines where the code is inserted. `code` is the code in the Device’s language. Here is an example for the C++ Standalone Device:
    
    
    device.insert_code('main', '''
    cout << "Testing direct insertion of code." << endl;
    ''')
    

For the C++ Standalone Device, all code is inserted into the `main.cpp` file, here into the `main` slot, referring to the main simulation function. This is a simplified version of this function in `main.cpp`:
    
    
    int main(int argc, char **argv)
    {
        // before_start
        brian_start();
        // after_start
    
        {{main_lines}}
    
        // before_end
        brian_end();
        // after_end
    
        return 0;
    }
    

`{{main_lines}}` is replaced in the generated code with the actual simulation. Code inserted into the `main` slot will be placed within the `{{main_lines}}`. `brian_start` allocates and initializes all arrays needed during the simulation and `brian_end` writes the results to disc and deallocates memory. Within the `{{main_lines}}`, all `Network` objects defined in Python are created and run. Code inserted in the `before/after_network_run` slot will be inserted around the `Network.run` call, which starts the time loop. Note that if your Python script has multiple `Network` objects or multiple `run` calls, code in the `before/after_network_run` slot will be inserted around each `Network.run` call in the generated code.

The code injection mechanism has been used for benchmarking experiments, see e.g. [here for Brian2CUDA benchmarks](https://github.com/brian-team/brian2cuda/blob/835c978ad758bc0621e34344c1fb7b811ef8a118/brian2cuda/tests/features/cuda_configuration.py#L148-L156) or [here for Brian2GeNN benchmarks](https://github.com/brian-team/brian2genn_benchmarks/blob/6d1a6d9d97c05653cec2e413c9fd312cfe13e15c/benchmark_utils.py#L78-L136).

### Customizing the build process

In standalone mode, a standard “make file” is used to orchestrate the compilation and linking. To provide additional arguments to the `make` command (respectively `nmake` on Windows), you can use the [devices.cpp_standalone.extra_make_args_unix](../advanced/preferences.html#brian-pref-devices-cpp-standalone-extra-make-args-unix) or [devices.cpp_standalone.extra_make_args_windows](../advanced/preferences.html#brian-pref-devices-cpp-standalone-extra-make-args-windows) preference. On Linux, this preference is by default set to `['-j']` to enable parallel compilation. Note that you can also use these arguments to overwrite variables in the make file, e.g. to use [clang](https://clang.llvm.org/) instead of the default [gcc](https://gcc.gnu.org/) compiler:
    
    
    prefs.devices.cpp_standalone.extra_make_args_unix += ['CC=clang++']
    

### Cleaning up after a run

Standalone simulations store all results of a simulation (final state variable values and values stored in monitors) to disk. These results can take up quite significant amount of space, and you might therefore want to delete these results when you do not need them anymore. You can do this by using the device’s [`delete`](../reference/brian2.devices.device.Device.html#brian2.devices.device.Device.delete "brian2.devices.device.Device.delete") method:
    
    
    device.delete()
    

Be aware that deleting the data will make all access to state variables fail, including the access to values in monitors. You should therefore only delete the data after doing all analysis/plotting that you are interested in.

By default, this function will delete both the generated code and the data, i.e. the full project directory. If you want to keep the code (which typically takes up little space compared to the results), exclude it from the deletion:
    
    
    device.delete(code=False)
    

If you added any additional files to the project directory manually, these will not be deleted by default. To delete the full directory regardless of its content, use the `force` option:
    
    
    device.delete(force=True)
    

Note

When you initialize state variables with concrete values (and not with a string expression), they will be stored to disk from your Python script and loaded from disk at the beginning of the standalone run. Since these values are necessary for the compiled binary file to run, they are considered “code” from the point of view of the [`delete`](../reference/brian2.devices.device.Device.html#brian2.devices.device.Device.delete "brian2.devices.device.Device.delete") function.

## Compiler settings

If using C++ code generation (either via cython or standalone), the compiler settings can make a big difference for the speed of the simulation. By default, Brian uses a set of compiler settings that switches on various optimizations and compiles for running on the same architecture where the code is compiled. This allows the compiler to make use of as many advanced instructions as possible, but reduces portability of the generated executable (which is not usually an issue).

If there are any issues with these compiler settings, for example because you are using an older version of the C++ compiler or because you want to run the generated code on a different architecture, you can change the settings by manually specifying the [codegen.cpp.extra_compile_args](../reference/brian2.codegen.html#brian-pref-codegen-cpp-extra-compile-args) preference (or by using [codegen.cpp.extra_compile_args_gcc](../reference/brian2.codegen.html#brian-pref-codegen-cpp-extra-compile-args-gcc) or [codegen.cpp.extra_compile_args_msvc](../reference/brian2.codegen.html#brian-pref-codegen-cpp-extra-compile-args-msvc) if you want to specify the settings for either compiler only).

---

# Converting from integrated form to ODEs2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/user/converting_from_integrated_form.html

# Converting from integrated form to ODEs

Brian requires models to be expressed as systems of first order ordinary differential equations, and the effect of spikes to be expressed as (possibly delayed) one-off changes. However, many neuron models are given in _integrated form_. For example, one form of the Spike Response Model (SRM; Gerstner and Kistler 2002) is defined as

\\[V(t) = \sum_i w_i \sum_{t_i} \mathrm{PSP}(t-t_i)+V_\mathrm{rest}\\]

where \\(V(t)\\) is the membrane potential, \\(V_\mathrm{rest}\\) is the rest potential, \\(w_i\\) is the synaptic weight of synapse \\(i\\), and \\(t_i\\) are the timings of the spikes coming from synapse \\(i\\), and PSP is a postsynaptic potential function.

An example PSP is the \\(\alpha\\)-function \\(\mathrm{PSP}(t)=(t/\tau)e^{-t/\tau}\\). For this function, we could rewrite the equation above in the following ODE form:

\\[\begin{split}\tau \frac{\mathrm{d}V}{\mathrm{d}t} & = V_\mathrm{rest}-V+g \\\ \tau \frac{\mathrm{d}g}{\mathrm{d}t} &= -g \\\ g &\leftarrow g+w_i\;\;\;\mbox{upon spike from synapse $i$}\end{split}\\]

This could then be written in Brian as:
    
    
    eqs = '''
    dV/dt = (V_rest-V+g)/tau : 1
    dg/dt = -g/tau : 1
    '''
    G = NeuronGroup(N, eqs, ...)
    ...
    S = Synapses(G, G, 'w : 1', on_pre='g += w')
    

To see that these two formulations are the same, you first solve the problem for the case of a single synapse and a single spike at time 0. The initial conditions at \\(t=0\\) will be \\(V(0)=V_\mathrm{rest}\\), \\(g(0)=w\\).

To solve these equations, let’s substitute \\(s=t/\tau\\) and take derivatives with respect to \\(s\\) instead of \\(t\\), set \\(u=V-V_\mathrm{rest}\\), and assume \\(w=1\\). This gives us the equations \\(u^\prime=g-u\\), \\(g^\prime=-g\\) with initial conditions \\(u(0)=0\\), \\(g(0)=1\\). At this point, you can either consult a textbook on solving linear systems of differential equations, or just [plug this into Wolfram Alpha](https://www.wolframalpha.com/input/?i=u%27\(s\)%3Dg\(s\)-u\(s\),+g%27\(s\)%3D-g\(s\),+u\(0\)%3D0,+g\(0\)%3D1) to get the solution \\(g(s)=e^{-s}\\), \\(u(s)=se^{-s}\\) which is equal to the PSP given above.

Now we use the linearity of these differential equations to see that it also works when \\(w\neq 0\\) and for summing over multiple spikes at different times.

In general, to convert from integrated form to ODE form, see [Köhn and Wörgötter (1998)](http://www.mitpressjournals.org/doi/abs/10.1162/089976698300017061), [Sánchez-Montañás (2001)](https://link.springer.com/chapter/10.1007/3-540-45720-8_14), and [Jahnke et al. (1999)](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.20.2284&rep=rep1&type=pdf). However, for some simple and widely used types of synapses, use the list below. In this list, we assume synapses are postsynaptic potentials, but you can replace \\(V(t)\\) with a current or conductance for postsynaptic currents or conductances. In each case, we give the Brian code with unitless variables, where `eqs` is the differential equations for the target [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup"), and `on_pre` is the argument to [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses").

**Exponential synapse** \\(V(t)=e^{-t/\tau}\\):
    
    
    eqs = '''
    dV/dt = -V/tau : 1
    '''
    on_pre = 'V += w'
    

**Alpha synapse** \\(V(t)=(t/\tau)e^{-t/\tau}\\):
    
    
    eqs = '''
    dV/dt = (x-V)/tau : 1
    dx/dt = -x/tau    : 1
    '''
    on_pre = 'x += w'
    

\\(V(t)\\) reaches a maximum value of \\(w/e\\) at time \\(t=\tau\\).

**Biexponential synapse** \\(V(t)=\frac{\tau_2}{\tau_2-\tau_1}\left(e^{-t/\tau_1}-e^{-t/\tau_2}\right)\\):
    
    
    eqs = '''
    dV/dt = ((tau_2 / tau_1) ** (tau_1 / (tau_2 - tau_1))*x-V)/tau_1 : 1
    dx/dt = -x/tau_2                                                 : 1
    '''
    on_pre = 'x += w'
    

\\(V(t)\\) reaches a maximum value of \\(w\\) at time \\(t=\frac{\tau_1\tau_2}{\tau_2-\tau_1}\log\left(\frac{\tau_2}{\tau_1}\right)\\).

**STDP**

The weight update equation of the standard STDP is also often stated in an integrated form and can be converted to an ODE form. This is covered in [Tutorial 2](../resources/tutorials/2-intro-to-brian-synapses.html).

---

# Custom events2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/advanced/custom_events.html

# Custom events  
  
## Overview

In most simulations, a [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") defines a threshold on its membrane potential that triggers a spike event. This event can be monitored by a [`SpikeMonitor`](../reference/brian2.monitors.spikemonitor.SpikeMonitor.html#brian2.monitors.spikemonitor.SpikeMonitor "brian2.monitors.spikemonitor.SpikeMonitor"), it is used in synaptic interactions, and in integrate-and-fire models it also leads to the execution of one or more reset statements.

Sometimes, it can be useful to define additional events, e.g. when an ion concentration in the cell crosses a certain threshold. This can be done with the custom events system in Brian, which is illustrated in this diagram.

![../_images/custom_events.svg](../_images/custom_events.svg)

You can see in this diagram that the source [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") has four types of events, called `spike`, `evt_other`, `evt_mon` and `evt_run`. The event `spike` is the default event. It is triggered when you you include `threshold='...'` in a [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup"), and has two potential effects. Firstly, when the event is triggered it causes the reset code to run, specified by `reset='...'`. Secondly, if there are [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses") connected, it causes the `on_pre` on `on_post` code to run (depending if the [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") is presynaptic or postsynaptic for those [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses")).

In the diagram though, we have three additional event types. We’ve included several event types here to make it clearer, but you could use the same event for different purposes. Let’s start with the first one, `evt_other`. To understand this, we need to look at the [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses") object in a bit more detail. A [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses") object has multiple _pathways_ associated to it. By default, there are just two, called `pre` and `post`. The `pre` pathway is activated by presynaptic spikes, and the `post` pathway by postsynaptic spikes. Specifically, the `spike` event on the presynaptic [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") triggers the `pre` pathway, and the `spike` event on the postsynaptic [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") triggers the `post` pathway. In the example in the diagram, we have created a new pathway called `other`, and the `evt_other` event in the presynaptic [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") triggers this pathway. Note that we can arrange this however we want. We could have `spike` trigger the `other` pathway if we wanted to, or allow it to trigger both the `pre` and `other` pathways. We could also allow `evt_other` to trigger the `pre` pathway. See below for details on the syntax for this.

The third type of event in the example is named `evt_mon` and this is connected to an [`EventMonitor`](../reference/brian2.monitors.spikemonitor.EventMonitor.html#brian2.monitors.spikemonitor.EventMonitor "brian2.monitors.spikemonitor.EventMonitor") which works exactly the same way as [`SpikeMonitor`](../reference/brian2.monitors.spikemonitor.SpikeMonitor.html#brian2.monitors.spikemonitor.SpikeMonitor "brian2.monitors.spikemonitor.SpikeMonitor") (which is just an [`EventMonitor`](../reference/brian2.monitors.spikemonitor.EventMonitor.html#brian2.monitors.spikemonitor.EventMonitor "brian2.monitors.spikemonitor.EventMonitor") attached by default to the event `spike`).

Finally, the fourth type of event in the example is named `evt_run`, and this causes some code to be run in the [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") triggered by the event. To add this code, we call [`NeuronGroup.run_on_event`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup.run_on_event "brian2.groups.neurongroup.NeuronGroup.run_on_event"). So, when you set `reset='...'`, this is equivalent to calling [`NeuronGroup.run_on_event`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup.run_on_event "brian2.groups.neurongroup.NeuronGroup.run_on_event") with the `spike` event.

## Details

### Defining an event

This can be done with the `events` keyword in the [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") initializer:
    
    
    group = NeuronGroup(N, '...', threshold='...', reset='...',
                        events={'custom_event': 'x > x_th'})
    

In this example, we define an event with the name `custom_event` that is triggered when the `x` variable crosses the threshold `x_th`. Note that you can define any number of custom events. Each event is defined by its name as the key, and its condition as the value of the dictionary.

### Recording events

Custom events can be recorded with an [`EventMonitor`](../reference/brian2.monitors.spikemonitor.EventMonitor.html#brian2.monitors.spikemonitor.EventMonitor "brian2.monitors.spikemonitor.EventMonitor"):
    
    
    event_mon = EventMonitor(group, 'custom_event')
    

Such an [`EventMonitor`](../reference/brian2.monitors.spikemonitor.EventMonitor.html#brian2.monitors.spikemonitor.EventMonitor "brian2.monitors.spikemonitor.EventMonitor") can be used in the same way as a [`SpikeMonitor`](../reference/brian2.monitors.spikemonitor.SpikeMonitor.html#brian2.monitors.spikemonitor.SpikeMonitor "brian2.monitors.spikemonitor.SpikeMonitor") – in fact, creating the [`SpikeMonitor`](../reference/brian2.monitors.spikemonitor.SpikeMonitor.html#brian2.monitors.spikemonitor.SpikeMonitor "brian2.monitors.spikemonitor.SpikeMonitor") is basically identical to recording the `spike` event with an [`EventMonitor`](../reference/brian2.monitors.spikemonitor.EventMonitor.html#brian2.monitors.spikemonitor.EventMonitor "brian2.monitors.spikemonitor.EventMonitor"). An [`EventMonitor`](../reference/brian2.monitors.spikemonitor.EventMonitor.html#brian2.monitors.spikemonitor.EventMonitor "brian2.monitors.spikemonitor.EventMonitor") is not limited to record the event time/neuron index, it can also record other variables of the model at the time of the event:
    
    
    event_mon = EventMonitor(group, 'custom_event', variables['var1', 'var2'])
    

### Triggering [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") code

If the event should trigger a series of statements (i.e. the equivalent of `reset` statements), this can be added by calling `run_on_event`:
    
    
    group.run_on_event('custom_event', 'x=0')
    

### Triggering synaptic pathways

When neurons are connected by [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses"), the `pre` and `post` pathways are triggered by `spike` events on the presynaptic and postsynaptic [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") by default. It is possible to change which pathway is triggered by which event by providing an `on_event` keyword that either specifies which event to use for all pathways, or a specific event for each pathway (where non-specified pathways use the default `spike` event):
    
    
    synapse_1 = Synapses(group, another_group, '...', on_pre='...', on_event='custom_event')
    

The code above causes all pathways to be triggered by an event named `custom_event` instead of the default `spike`.
    
    
    synapse_2 = Synapses(group, another_group, '...', on_pre='...', on_post='...',
                         on_event={'pre': 'custom_event'})
    

In the code above, only the `pre` pathway is triggered by the `custom_event` event.

We can also create new pathways and have them be triggered by custom events. For example:
    
    
    synapse_3 = Synapses(group, another_group, '...',
                         on_pre={'pre': '....',
                                 'custom_pathway': '...'},
                         on_event={'pre': 'spike',
                                   'custom_pathway': 'custom_event'})
    

In this code, the default `pre` pathway is still triggered by the `spike` event, but there is a new pathway called `custom_pathway` that is triggered by the `custom_event` event.

### Scheduling

By default, custom events are checked after the spiking threshold (in the `after_thresholds` slots) and statements are executed after the reset (in the `after_resets` slots). The slot for the execution of custom event-triggered statements can be changed when it is added with the usual `when` and `order` keyword arguments (see [Scheduling](../user/running.html#scheduling) for details). To change the time when the condition is checked, use [`NeuronGroup.set_event_schedule`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup.set_event_schedule "brian2.groups.neurongroup.NeuronGroup.set_event_schedule").

---

# Custom progress reporting2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/advanced/scheduling.html

# Custom progress reporting

## Progress reporting

For custom progress reporting (e.g. graphical output, writing to a file, etc.), the `report` keyword accepts a callable (i.e. a function or an object with a `__call__` method) that will be called with four parameters:

  * `elapsed`: the total (real) time since the start of the run

  * `completed`: the fraction of the total simulation that is completed, i.e. a value between 0 and 1

  * `start`: The start of the simulation (in biological time)

  * `duration`: the total duration (in biological time) of the simulation

The function will be called every `report_period` during the simulation, but also at the beginning and end with `completed` equal to 0.0 and 1.0, respectively.

For the C++ standalone mode, the same standard options are available. It is also possible to implement custom progress reporting by directly passing the code (as a multi-line string) to the `report` argument. This code will be filled into a progress report function template, it should therefore only contain a function body. The simplest use of this might look like:
    
    
    net.run(duration, report='std::cout << (int)(completed*100.) << "% completed" << std::endl;')
    

### Examples of custom reporting

**Progress printed to a file**
    
    
    from brian2.core.network import TextReport
    report_file = open('report.txt', 'w')
    file_reporter = TextReport(report_file)
    net.run(duration, report=file_reporter)
    report_file.close()
    

**“Graphical” output on the console**

This needs a “normal” Linux console, i.e. it might not work in an integrated console in an IDE.

Adapted from <http://stackoverflow.com/questions/3160699/python-progress-bar>
    
    
    import sys
    
    class ProgressBar(object):
        def __init__(self, toolbar_width=40):
            self.toolbar_width = toolbar_width
            self.ticks = 0
    
        def __call__(self, elapsed, complete, start, duration):
            if complete == 0.0:
                # setup toolbar
                sys.stdout.write("[%s]" % (" " * self.toolbar_width))
                sys.stdout.flush()
                sys.stdout.write("\b" * (self.toolbar_width + 1)) # return to start of line, after '['
            else:
                ticks_needed = int(round(complete * self.toolbar_width))
                if self.ticks < ticks_needed:
                    sys.stdout.write("-" * (ticks_needed-self.ticks))
                    sys.stdout.flush()
                    self.ticks = ticks_needed
            if complete == 1.0:
                sys.stdout.write("\n")
    
    net.run(duration, report=ProgressBar(), report_period=1*second)
    

**“Standalone Mode” Text based progress bar on console**

This needs a “normal” Linux console, i.e. it might not work in an integrated console in an IDE.

Adapted from <https://stackoverflow.com/questions/14539867/how-to-display-a-progress-indicator-in-pure-c-c-cout-printf>
    
    
    set_device('cpp_standalone')
    
    report_func = '''
        int remaining = (int)((1-completed)/completed*elapsed+0.5);
        if (completed == 0.0)
        {
            std::cout << "Starting simulation at t=" << start << " s for duration " << duration << " s"<<std::flush;
        }
        else
        {
            int barWidth = 70;
            std::cout << "\\r[";
            int pos = barWidth * completed;
            for (int i = 0; i < barWidth; ++i) {
                    if (i < pos) std::cout << "=";
                    else if (i == pos) std::cout << ">";
                    else std::cout << " ";
            }
            std::cout << "] " << int(completed * 100.0) << "% completed. | "<<int(remaining) <<"s remaining"<<std::flush;
        }
    '''
    run(100*second, report=report_func)
    

---

# Devices2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/developer/devices.html

# Devices

This document describes how to implement a new `Device` for Brian. This is a somewhat complicated process, and you should first be familiar with devices from the user point of view ([Computational methods and efficiency](../user/computation.html)) as well as the code generation system ([Code generation](codegen.html)).

We wrote Brian’s devices system to allow for two major use cases, although it can potentially be extended beyond this. The two use cases are:

  1. Runtime mode. In this mode, everything is managed by Python, including memory management (using numpy by default) and running the simulation. Actual computational work can be carried out in several different ways, including numpy or Cython.

  2. Standalone mode. In this mode, running a Brian script leads to generating an entire source code project tree which can be compiled and run independently of Brian or Python.

Runtime mode is handled by `RuntimeDevice` and is already implemented, so here I will mainly discuss standalone devices. A good way to understand these devices is to look at the implementation of `CPPStandaloneDevice` (the only one implemented in the core of Brian). In many cases, the simplest way to implement a new standalone device would be to derive a class from `CPPStandaloneDevice` and overwrite just a few methods.

## Memory management

Memory is managed primarily via the `Device.add_array`, `Device.get_value` and `Device.set_value` methods. When a new array is created, the `add_array` method is called, and when trying to access this memory the other two are called. The `RuntimeDevice` uses numpy to manage the memory and returns the underlying arrays in these methods. The `CPPStandaloneDevice` just stores a dictionary of array names but doesn’t allocate any memory. This information is later used to generate code that will allocate the memory, etc.

## Code objects

As in the case of runtime code generation, computational work is done by a collection of `CodeObject` s. In `CPPStandaloneDevice`, each code object is converted into a pair of `.cpp` and `.h` files, and this is probably a fairly typical way to do it.

## Building

The method `Device.build` is used to generate the project. This can be implemented any way you like, although looking at `CPPStandaloneDevice.build` is probably a good way to get an idea of how to do it.

## Device override methods

Several functions and methods in Brian are decorated with the `device_override` decorator. This mechanism allows a standalone device to override the behaviour of any of these functions by implementing a method with the name provided to `device_override`. For example, the `CPPStandaloneDevice` uses this to override [`Network.run`](../reference/brian2.core.network.Network.html#brian2.core.network.Network.run "brian2.core.network.Network.run") as `CPPStandaloneDevice.network_run`.

## Other methods

There are some other methods to implement, including initialising arrays, creating spike queues for synaptic propagation. Take a look at the source code for these.

---

# Equations and namespaces2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/developer/equations_namespaces.html

# Equations and namespaces

## Equation parsing

Parsing is done via [pyparsing](https://pythonhosted.org/pyparsing/pyparsing-module.html), for now find the grammar at the top of the [`brian2.equations.equations`](../reference/brian2.equations.html#module-brian2.equations.equations "brian2.equations.equations") file.

## Variables

Each Brian object that saves state variables (e.g. [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup"), [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses"), [`StateMonitor`](../reference/brian2.monitors.statemonitor.StateMonitor.html#brian2.monitors.statemonitor.StateMonitor "brian2.monitors.statemonitor.StateMonitor")) has a `variables` attribute, a dictionary mapping variable names to `Variable` objects (in fact a `Variables` object, not a simple dictionary). `Variable` objects contain information _about_ the variable (name, dtype, units) as well as access to the variable’s value via a `get_value` method. Some will also allow setting the values via a corresponding `set_value` method. These objects can therefore act as proxies to the variables’ “contents”.

`Variable` objects provide the “abstract namespace” corresponding to a chunk of “abstract code”, they are all that is needed to check for syntactic correctness, unit consistency, etc.

## Namespaces

The `namespace` attribute of a group can contain information about the external (variable or function) names used in the equations. It specifies a group-specific namespace used for resolving names in that group. At run time, this namespace is combined with a “run namespace”. This namespace is either explicitly provided to the [`Network.run`](../reference/brian2.core.network.Network.html#brian2.core.network.Network.run "brian2.core.network.Network.run") method, or the implicit namespace consisting of the locals and globals around the point where the run function is called is used. This namespace is then passed down to all the objects via `Network.before_fun` which calls all the individual [`BrianObject.before_run`](../reference/brian2.core.base.BrianObject.html#brian2.core.base.BrianObject.before_run "brian2.core.base.BrianObject.before_run") methods with this namespace.

---

# Equations2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/user/equations.html

# Equations

  * Equation strings

  * Arithmetic operations and functions

  * Special variables

  * External references

  * Flags

  * List of special symbols

  * Event-driven equations

  * Equation objects

  * Examples of `Equation` objects

## Equation strings

Equations are used both in [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") and [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses") to:

  * define state variables

  * define continuous-updates on these variables, through differential equations

Note

Brian models are defined by systems of first order ordinary differential equations, but you might see the integrated form of synapses in some textbooks and papers. See [Converting from integrated form to ODEs](converting_from_integrated_form.html) for details on how to convert between these representations.

Equations are defined by multiline strings, where each line takes of one of three forms:

  1. `dx/dt = f : unit (flags)` (differential equation)

  2. `x = f : unit (flags)` (subexpression)

  3. `x : unit (flags)` (parameter)

Each of these definitions can take optional `flags` in parentheses after the `unit` declaration (see Flags below).

The first form defines a differential equation that determines how a variable evolves over time. The second form defines a subexpression, which is useful to make complex equations more readable, and to have a name for expressions that can be recorded with a [`StateMonitor`](../reference/brian2.monitors.statemonitor.StateMonitor.html#brian2.monitors.statemonitor.StateMonitor "brian2.monitors.statemonitor.StateMonitor"). Such subexpressions are computed “on demand” and are not stored. Their use is therefore mostly for convenience and does not affect simulation time or memory usage. The third form defines a parameter, which is a value that is unique to each neuron or synapse. Its value can either be constant (e.g. to have a heterogeneous population of neurons) or can be a value that gets updated by synaptic events, or by [`run_regularly`](../reference/brian2.groups.group.Group.html#brian2.groups.group.Group.run_regularly "brian2.groups.group.Group.run_regularly") operations.

Each definition may be spread out over multiple lines to improve readability, and can include comments after `#`. The `unit` definition defines the dimension of the variable. Note that these are always the dimensions of the _variable_ defined in the line, even in the case of differential equations. Therefore, the unit for the membrane potential would be `volt` and not `volt/second` (the dimensions of its derivative). The `unit` always has to be a _base unit_ , i.e., one must write `volt`, not `mV`. This is to make it clear that the values are internally always saved in the base units, so no confusion can arise when getting the values out of a [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") and discarding the units. Compound units are of course allowed as well (e.g. `farad/meter**2`). There are also three special “units” that can be used: `1` denotes a dimensionless floating point variable, `boolean` and `integer` denote dimensionless variables of the respective kind.

Note

For molar concentration, the base unit that has to be used in the equations is `mmolar` (or `mM`), _not_ `molar`. This is because 1 molar is 10³ mol/m³ in SI units (i.e., it has a “scale” of 10³), whereas 1 millimolar corresponds to 1 mol/m³.

## Arithmetic operations and functions

Equation strings can make use of standard arithmetic operations for numerical values, using the Python 3 syntax. The supported operations are `+`, `-`, `*`, `/` (floating point division), `//` (flooring division), `%` (remainder), `**` (power). For variable assignments, e.g. in reset statements, the corresponding in-place assignments such as `+=` can be used as well. For comparisons, the operations `==` (equality), `!=` (inequality), `<`, `<=`, `>`, and `>=` are available. Truth values can be combined using `and` and `or`, or negated using `not`. Note that Brian does not support any operations specific to integers, e.g. “bitwise AND” or shift operations. Importantly, while equations use Python syntax, they are not Python code; they are parsed and translated to the target language by Brian, and can therefore not use arbitrary Python syntax or functions. They are also written in a “for each neuron/synapse” style, so their interpretation depends on the context in which they are used. For example, when a synaptic pre/post statement refers to a variable of a pre- or post-synaptic neurons, it only refers to the subset of neurons that spiked. This also means that you cannot (and usually don’t need to) use Python’s indexing syntax to refer to specific elements of a group.

Warning

Brian versions up to 2.1.3.1 did not support `//` as the floor division operator and potentially used different semantics for the `/` operator depending on whether Python 2 or 3 was used. To write code that correctly and unambiguously works with both newer and older Brian versions, you can use expressions such as `1.0*a/b` to enforce floating point division (if one of the operands is a floating point number, both Python 2 and 3 will use floating point division), or `floor(a/b)` to enforce flooring division Note that the `floor` function always returns a floating point value, if it is important that the result is an integer value, additionally wrap it with the `int` function.

Brian also supports standard mathematical functions with the same names as used in the `numpy` library (e.g. `exp`, `sqrt`, `abs`, `clip`, `sin`, `cos`, …) – for a full list see [Default functions](../advanced/functions.html#default-functions). Note that support for such functions is provided by Brian itself and the translation to the various code generation targets is automatically taken care of. You should therefore refer to them directly by name and not as e.g. `np.sqrt` or `numpy.sqrt`, regardless of the way you [imported Brian or numpy](import.html). This also means that you cannot directly refer to arbitrary functions from `numpy` or other libraries. For details on how to extend the support to non-default functions see [User-provided functions](../advanced/functions.html#user-functions).

## Special variables

Some special variables are defined, e.g. `t`, `dt` (time) and `xi` (white noise). For a full list see List of special symbols below. Variable names starting with an underscore and a couple of other names that have special meanings under certain circumstances (e.g. names ending in `_pre` or `_post`) are forbidden.

For stochastic equations with several `xi` values it is necessary to make clear whether they correspond to the same or different noise instantiations. To make this distinction, an arbitrary suffix can be used, e.g. using `xi_1` several times refers to the same variable, `xi_2` (or `xi_inh`, `xi_alpha`, etc.) refers to another. An error will be raised if you use more than one plain `xi` without any suffix. Note that noise is always independent across neurons, you can only work around this restriction by defining your noise variable as a shared parameter and update it using a user-defined function (e.g. with `run_regularly`), or create a group that models the noise and link to its variable (see [Linked variables](models.html#linked-variables)).

## External references

Equations defining neuronal or synaptic equations can contain references to external constants or functions. These references are looked up at the time that the simulation is run. If you don’t specify where to look them up, it will look in the Python local/global namespace (i.e. the block of code where you call [`run()`](../reference/brian2.core.magic.run.html#brian2.core.magic.run "brian2.core.magic.run")). If you want to override this, you can specify an explicit “namespace”. This is a Python dictionary with keys being variable names as they appear in the equations, and values being the desired value of that variable. This namespace can be specified either in the creation of the group or when you can the [`run()`](../reference/brian2.core.magic.run.html#brian2.core.magic.run "brian2.core.magic.run") function using the `namespace` keyword argument.

The following three examples show the different ways of providing external variable values, all having the same effect in this case:
    
    
    # Explicit argument to the NeuronGroup
    G = NeuronGroup(1, 'dv/dt = -v / tau : 1', namespace={'tau': 10*ms})
    net = Network(G)
    net.run(10*ms)
    
    # Explicit argument to the run function
    G = NeuronGroup(1, 'dv/dt = -v / tau : 1')
    net = Network(G)
    net.run(10*ms, namespace={'tau': 10*ms})
    
    # Implicit namespace from the context
    G = NeuronGroup(1, 'dv/dt = -v / tau : 1')
    net = Network(G)
    tau = 10*ms
    net.run(10*ms)
    

See [Namespaces](../advanced/namespaces.html) for more details.

The following topics are not essential for beginners.

  

## Flags

A _flag_ is a keyword in parentheses at the end of the line, which qualifies the equations. There are several keywords:

_event-driven_
    

this is only used in Synapses, and means that the differential equation should be updated only at the times of events. This implies that the equation is taken out of the continuous state update, and instead a event-based state update statement is generated and inserted into event codes (pre and post). This can only qualify differential equations of synapses. Currently, only one-dimensional linear equations can be handled (see below).

_unless refractory_
    

this means the variable is not updated during the refractory period. This can only qualify differential equations of neuron groups.

_constant_
    

this means the parameter will not be changed during a run. This allows optimizations in state updaters. This can only qualify parameters.

_constant over dt_
    

this means that the subexpression will be only evaluated once at the beginning of the time step. This can be useful to e.g. approximate a non-linear term as constant over a time step in order to use the `linear` numerical integration algorithm. It is also mandatory for subexpressions that refer to stateful functions like `rand()` to make sure that they are only evaluated once (otherwise e.g. recording the value with a [`StateMonitor`](../reference/brian2.monitors.statemonitor.StateMonitor.html#brian2.monitors.statemonitor.StateMonitor "brian2.monitors.statemonitor.StateMonitor") would re-evaluate it and therefore not record the same values that are used in other places). This can only qualify subexpressions.

_shared_
    

this means that a parameter or subexpression is not neuron-/synapse-specific but rather a single value for the whole [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") or [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses"). A shared subexpression can only refer to other shared variables.

_linked_
    

this means that a parameter refers to a parameter in another [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup"). See [Linked variables](models.html#linked-variables) for more details.

Multiple flags may be specified as follows:
    
    
    dx/dt = f : unit (flag1,flag2)
    

## List of special symbols

The following lists all of the special symbols that Brian uses in equations and code blocks, and their meanings.

dt
    

Time step width

i
    

Index of a neuron ([`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup")) or the pre-synaptic neuron of a synapse ([`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses"))

j
    

Index of a post-synaptic neuron of a synapse

lastspike
    

Last time that the neuron spiked (for refractoriness)

lastupdate
    

Time of the last update of synaptic variables in event-driven equations (only defined when event-driven equations are used).

N
    

Number of neurons ([`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup")) or synapses ([`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses")). Use `N_pre` or `N_post` for the number of presynaptic or postsynaptic neurons in the context of [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses").

not_refractory
    

Boolean variable that is normally true, and false if the neuron is currently in a refractory state

t
    

Current time

t_in_timesteps
    

Current time measured in time steps

xi, xi_*
    

Stochastic differential in equations

## Event-driven equations

Equations defined as event-driven are completely ignored in the state update. They are only defined as variables that can be externally accessed. There are additional constraints:

  * An event-driven variable cannot be used by any other equation that is not also event-driven.

  * An event-driven equation cannot depend on a differential equation that is not event-driven (directly, or indirectly through subexpressions). It can depend on a constant parameter.

Currently, automatic event-driven updates are only possible for one-dimensional linear equations, but this may be extended in the future.

## Equation objects

The model definitions for [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") and [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses") can be simple strings or [`Equations`](../reference/brian2.equations.equations.Equations.html#brian2.equations.equations.Equations "brian2.equations.equations.Equations") objects. Such objects can be combined using the add operator:
    
    
    eqs = Equations('dx/dt = (y-x)/tau : volt')
    eqs += Equations('dy/dt = -y/tau: volt')
    

[`Equations`](../reference/brian2.equations.equations.Equations.html#brian2.equations.equations.Equations "brian2.equations.equations.Equations") allow for the specification of values in the strings, but does this by simple string replacement, e.g. you can do:
    
    
    eqs = Equations('dx/dt = x/tau : volt', tau=10*ms)
    

but this is exactly equivalent to:
    
    
    eqs = Equations('dx/dt = x/(10*ms) : volt')
    

The [`Equations`](../reference/brian2.equations.equations.Equations.html#brian2.equations.equations.Equations "brian2.equations.equations.Equations") object does some basic syntax checking and will raise an error if two equations defining the same variable are combined. It does not however do unit checking, checking for unknown identifiers or incorrect flags – all this will be done during the instantiation of a [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") or [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses") object.

## Examples of `Equation` objects

**Concatenating equations**
    
    
    >>> membrane_eqs = Equations('dv/dt = -(v + I)/ tau : volt')
    >>> eqs1 = membrane_eqs + Equations('''I = sin(2*pi*freq*t) : volt
    ...                                    freq : Hz''')
    >>> eqs2 = membrane_eqs + Equations('''I : volt''')
    >>> print(eqs1)
    I = sin(2*pi*freq*t) : V
    dv/dt = -(v + I)/ tau : V
    freq : Hz
    >>> print(eqs2)
    dv/dt = -(v + I)/ tau : V
    I : V
    

**Substituting variable names**
    
    
    >>> general_equation = 'dg/dt = -g / tau : siemens'
    >>> eqs_exc = Equations(general_equation, g='g_e', tau='tau_e')
    >>> eqs_inh = Equations(general_equation, g='g_i', tau='tau_i')
    >>> print(eqs_exc)
    dg_e/dt = -g_e / tau_e : S
    >>> print(eqs_inh)
    dg_i/dt = -g_i / tau_i : S
    

**Inserting values**
    
    
    >>> eqs = Equations('dv/dt = mu/tau + sigma/tau**.5*xi : volt',
    ...                  mu=-65*mV, sigma=3*mV, tau=10*ms)
    >>> print(eqs)
    dv/dt = (-65. * mvolt)/(10. * msecond) + (3. * mvolt)/(10. * msecond)**.5*xi : V
    

---

# Example: 01_using_cython2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/multiprocessing.01_using_cython.html

# Example: 01_using_cython

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/multiprocessing/01_using_cython.ipynb)

Parallel processes using Cython

This example use multiprocessing to run several simulations in parallel. The code is using the default runtime mode (and Cython compilation, if possible).

The `numb_proc` variable set the number of processes. `run_sim` is just a toy example that creates a single neuron and connects a [`StateMonitor`](../reference/brian2.monitors.statemonitor.StateMonitor.html#brian2.monitors.statemonitor.StateMonitor "brian2.monitors.statemonitor.StateMonitor") to record the voltage.

For more details see the [github issue 1154](https://github.com/brian-team/brian2/issues/1154#issuecomment-582994117):

Note that Python’s [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing "\(in Python v3.12\)") module cannot deal with user-defined functions (including [`TimedArray`](../reference/brian2.input.timedarray.TimedArray.html#brian2.input.timedarray.TimedArray "brian2.input.timedarray.TimedArray")) and other complex code structures. If you run into `PicklingError` or [`AttributeError`](https://docs.python.org/3/library/exceptions.html#AttributeError "\(in Python v3.12\)") exceptions, you might have to use the `pathos` (<https://pypi.org/project/pathos>) package instead, which can handle more complex code structures.
    
    
    import os
    import multiprocessing
    
    from brian2 import *
    
    
    def run_sim(tau):
        pid = os.getpid()
        print(f'RUNNING {pid}')
        G = NeuronGroup(1, 'dv/dt = -v/tau : 1', method='exact')
        G.v = 1
        mon = StateMonitor(G, 'v', record=0)
        run(100*ms)
        print(f'FINISHED {pid}')
        return mon.t/ms, mon.v[0]
    
    
    if __name__ == "__main__":
        num_proc = 4
    
        tau_values = np.arange(10)*ms + 5*ms
        with multiprocessing.Pool(num_proc) as p:
            results = p.map(run_sim, tau_values)
    
        for tau_value, (t, v) in zip(tau_values, results):
            plt.plot(t, v, label=str(tau_value))
        plt.legend()
        plt.show()
    

![../_images/multiprocessing.01_using_cython.1.png](../_images/multiprocessing.01_using_cython.1.png)

---

# Example: 02_using_standalone2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/multiprocessing.02_using_standalone.html

# Example: 02_using_standalone

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/multiprocessing/02_using_standalone.ipynb)

Parallel processes using standalone mode

This example use multiprocessing to run several simulations in parallel. The code is using the C++ standalone mode to compile and execute the code.

The generated code is stored in a `standalone{pid}` directory, with `pid` being the id of each process.

Note that the [`set_device()`](../reference/brian2.devices.device.set_device.html#brian2.devices.device.set_device "brian2.devices.device.set_device") call should be in the `run_sim` function.

By moving the [`set_device()`](../reference/brian2.devices.device.set_device.html#brian2.devices.device.set_device "brian2.devices.device.set_device") line into the parallelised function, it creates one C++ standalone device per process. The `device.reinit()` needs to be called` if you are running multiple simulations per process (there are 10 tau values and num_proc = 4).

Each simulation uses it’s own code folder to generate the code for the simulation, controlled by the directory keyword to the set_device call. By setting `directory=None`, a temporary folder with random name is created. This way, each simulation uses a different folder for code generation and there is nothing shared between the parallel processes.

If you don’t set the directory argument, it defaults to `directory="output"`. In that case each process would use the same files to try to generate and compile your simulation, which would lead to compile/execution errors.

Setting `directory=f"standalone{pid}"` is even better than using `directory=None` in this case. That is, giving each parallel process _it’s own directory to work on_. This way you avoid the problem of multiple processes working on the same code directories. But you also don’t need to recompile the entire project at each simulation. What happens is that in the generated code in two consecutive simulations in a single process will only differ slightly (in this case only the tau parameter). The compiler will therefore only recompile the file that has changed and not the entire project.

The `numb_proc` sets the number of processes. `run_sim` is just a toy example that creates a single neuron and connects a [`StateMonitor`](../reference/brian2.monitors.statemonitor.StateMonitor.html#brian2.monitors.statemonitor.StateMonitor "brian2.monitors.statemonitor.StateMonitor") to record the voltage.

For more details see the [discussion in the Brian forum](https://brian.discourse.group/t/multiprocessing-in-standalone-mode/142/2).

Note that Python’s [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing "\(in Python v3.12\)") module cannot deal with user-defined functions (including [`TimedArray`](../reference/brian2.input.timedarray.TimedArray.html#brian2.input.timedarray.TimedArray "brian2.input.timedarray.TimedArray")) and other complex code structures. If you run into `PicklingError` or [`AttributeError`](https://docs.python.org/3/library/exceptions.html#AttributeError "\(in Python v3.12\)") exceptions, you might have to use the `pathos` (<https://pypi.org/project/pathos>) package instead, which can handle more complex code structures.
    
    
    import os
    import multiprocessing
    from time import time as wall_time
    from os import system
    from brian2 import *
    
    def run_sim(tau):
        pid = os.getpid()
        directory = f"standalone{pid}"
        set_device('cpp_standalone', directory=directory)
        print(f'RUNNING {pid}')
    
        G = NeuronGroup(1, 'dv/dt = -v/tau : 1', method='euler')
        G.v = 1
    
        mon = StateMonitor(G, 'v', record=0)
        net = Network()
        net.add(G, mon)
        net.run(100 * ms)
        res = (mon.t/ms, mon.v[0])
    
        device.reinit()
    
        print(f'FINISHED {pid}')
        return res
    
    
    if __name__ == "__main__":
        start_time = wall_time()
    
        num_proc = 4
        tau_values = np.arange(10)*ms + 5*ms
        with multiprocessing.Pool(num_proc) as p:
            results = p.map(run_sim, tau_values)
    
        print(f"Done in {wall_time() - start_time:10.3f}")
    
        for tau_value, (t, v) in zip(tau_values, results):
            plt.plot(t, v, label=str(tau_value))
        plt.legend()
        plt.show()
    

![../_images/multiprocessing.02_using_standalone.1.png](../_images/multiprocessing.02_using_standalone.1.png)

---

# Example: 03_standalone_joblib2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/multiprocessing.03_standalone_joblib.html

# Example: 03_standalone_joblib

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/multiprocessing/03_standalone_joblib.ipynb)

This example use C++ standalone mode for the simulation and the [joblib library](https://joblib.readthedocs.io) to parallelize the code. See the previous example (`02_using_standalone.py`) for more explanations.
    
    
    from joblib import Parallel, delayed
    from time import time as wall_time
    from brian2 import *
    import os
    
    
    def run_sim(tau):
        pid = os.getpid()
        directory = f"standalone{pid}"
        set_device('cpp_standalone', directory=directory)
        print(f'RUNNING {pid}')
    
        G = NeuronGroup(1, 'dv/dt = -v/tau : 1', method='euler')
        G.v = 1
    
        mon = StateMonitor(G, 'v', record=0)
        net = Network()
        net.add(G, mon)
        net.run(100 * ms)
        res = (mon.t/ms, mon.v[0])
    
        device.reinit()
    
        print(f'FINISHED {pid}')
        return res
    
    
    if __name__ == "__main__":
        start_time = wall_time()
    
        n_jobs = 4
        tau_values = np.arange(10)*ms + 5*ms
    
        results = Parallel(n_jobs=n_jobs)(map(delayed(run_sim), tau_values))
    
        print(f"Done in {wall_time() - start_time:10.3f}")
    
        for tau_value, (t, v) in zip(tau_values, results):
            plt.plot(t, v, label=str(tau_value))
        plt.legend()
        plt.show()
    

![../_images/multiprocessing.03_standalone_joblib.1.png](../_images/multiprocessing.03_standalone_joblib.1.png)

---

# Example: COBAHH2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/COBAHH.html

# Example: COBAHH

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/COBAHH.ipynb)

This is an implementation of a benchmark described in the following review paper:

Simulation of networks of spiking neurons: A review of tools and strategies (2006). Brette, Rudolph, Carnevale, Hines, Beeman, Bower, Diesmann, Goodman, Harris, Zirpe, Natschläger, Pecevski, Ermentrout, Djurfeldt, Lansner, Rochel, Vibert, Alvarez, Muller, Davison, El Boustani and Destexhe. Journal of Computational Neuroscience

Benchmark 3: random network of HH neurons with exponential synaptic conductances

Clock-driven implementation (no spike time interpolation)

  18. Brette - Dec 2007

    
    
    from brian2 import *
    
    # Parameters
    area = 20000*umetre**2
    Cm = (1*ufarad*cm**-2) * area
    gl = (5e-5*siemens*cm**-2) * area
    
    El = -60*mV
    EK = -90*mV
    ENa = 50*mV
    g_na = (100*msiemens*cm**-2) * area
    g_kd = (30*msiemens*cm**-2) * area
    VT = -63*mV
    # Time constants
    taue = 5*ms
    taui = 10*ms
    # Reversal potentials
    Ee = 0*mV
    Ei = -80*mV
    we = 6*nS  # excitatory synaptic weight
    wi = 67*nS  # inhibitory synaptic weight
    
    # The model
    eqs = Equations('''
    dv/dt = (gl*(El-v)+ge*(Ee-v)+gi*(Ei-v)-
             g_na*(m*m*m)*h*(v-ENa)-
             g_kd*(n*n*n*n)*(v-EK))/Cm : volt
    dm/dt = alpha_m*(1-m)-beta_m*m : 1
    dn/dt = alpha_n*(1-n)-beta_n*n : 1
    dh/dt = alpha_h*(1-h)-beta_h*h : 1
    dge/dt = -ge*(1./taue) : siemens
    dgi/dt = -gi*(1./taui) : siemens
    alpha_m = 0.32*(mV**-1)*4*mV/exprel((13*mV-v+VT)/(4*mV))/ms : Hz
    beta_m = 0.28*(mV**-1)*5*mV/exprel((v-VT-40*mV)/(5*mV))/ms : Hz
    alpha_h = 0.128*exp((17*mV-v+VT)/(18*mV))/ms : Hz
    beta_h = 4./(1+exp((40*mV-v+VT)/(5*mV)))/ms : Hz
    alpha_n = 0.032*(mV**-1)*5*mV/exprel((15*mV-v+VT)/(5*mV))/ms : Hz
    beta_n = .5*exp((10*mV-v+VT)/(40*mV))/ms : Hz
    ''')
    
    P = NeuronGroup(4000, model=eqs, threshold='v>-20*mV', refractory=3*ms,
                    method='exponential_euler')
    Pe = P[:3200]
    Pi = P[3200:]
    Ce = Synapses(Pe, P, on_pre='ge+=we')
    Ci = Synapses(Pi, P, on_pre='gi+=wi')
    Ce.connect(p=0.02)
    Ci.connect(p=0.02)
    
    # Initialization
    P.v = 'El + (randn() * 5 - 5)*mV'
    P.ge = '(randn() * 1.5 + 4) * 10.*nS'
    P.gi = '(randn() * 12 + 20) * 10.*nS'
    
    # Record a few traces
    trace = StateMonitor(P, 'v', record=[1, 10, 100])
    run(1 * second, report='text')
    plot(trace.t/ms, trace[1].v/mV)
    plot(trace.t/ms, trace[10].v/mV)
    plot(trace.t/ms, trace[100].v/mV)
    xlabel('t (ms)')
    ylabel('v (mV)')
    show()
    

![../_images/COBAHH.1.png](../_images/COBAHH.1.png)

---

# Example: COBAHH_approximated2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/advanced.COBAHH_approximated.html

# Example: COBAHH_approximated

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/advanced/COBAHH_approximated.ipynb)

Follows exercise 4, chapter 2 of Eugene M. Izhikevich: Dynamical Systems in Neuroscience

Sebastian Schmitt, 2021
    
    
    import argparse
    from functools import reduce
    import operator
    
    import matplotlib.pyplot as plt
    from cycler import cycler
    import numpy as np
    
    from brian2 import run
    from brian2 import mS, cmeter, ms, mV, uA, uF
    from brian2 import Equations, NeuronGroup, StateMonitor, TimedArray, defaultclock
    
    
    def construct_gating_variable_inf_equation(gating_variable):
        """Construct the voltage-dependent steady-state gating variable equation.
    
        Approximated by Boltzmann function.
    
        gating_variable -- gating variable, typically one of "m", "n" and "h"
        """
    
        return Equations('xinf = 1/(1+exp((v_half-v)/k)) : 1',
                         xinf=f'{gating_variable}_inf',
                         v_half=f'v_{gating_variable}_half',
                         k=f'k_{gating_variable}')
    
    
    def construct_gating_variable_tau_equation(gating_variable):
        """Construct the voltage-dependent gating variable time constant equation.
    
        Approximated by Gaussian function.
    
        gating_variable -- gating variable, typically one of "m", "n" and "h"
        """
    
        return Equations('tau = c_base + c_amp*exp(-(v_max - v)**2/sigma**2) : second',
                         tau=f'tau_{gating_variable}',
                         c_base=f'c_{gating_variable}_base',
                         c_amp=f'c_{gating_variable}_amp',
                         v_max=f'v_{gating_variable}_max',
                         sigma=f'sigma_{gating_variable}')
    
    
    def construct_gating_variable_ode(gating_variable):
        """Construct the ordinary differential equation of the gating variable.
    
        gating_variable -- gating variable, typically one of "m", "n" and "h"
        """
    
        return Equations('dx/dt = (xinf - x)/tau : 1',
                         x=gating_variable,
                         xinf=f'{gating_variable}_inf',
                         tau=f'tau_{gating_variable}')
    
    
    def construct_neuron_ode():
        """Construct the ordinary differential equation of the membrane."""
    
        # conductances
        g_K_eq = Equations('g_K = g_K_bar*n**4 : siemens/meter**2')
        g_Na_eq = Equations('g_Na = g_Na_bar*m**3*h : siemens/meter**2')
    
        # currents
        I_K_eq = Equations('I_K = g_K*(v - e_K) : ampere/meter**2')
        I_Na_eq = Equations('I_Na = g_Na*(v - e_Na) : ampere/meter**2')
        I_L_eq = Equations('I_L = g_L*(v - e_L) : ampere/meter**2')
    
        # external drive
        I_ext_eq = Equations('I_ext = I_stim(t) : ampere/meter**2')
    
        # membrane
        membrane_eq = Equations('dv/dt = (I_ext - I_K - I_Na - I_L)/C_mem : volt')
    
        return [g_K_eq, g_Na_eq, I_K_eq, I_Na_eq, I_L_eq, I_ext_eq, membrane_eq]
    
    
    def plot_tau(ax, parameters):
        """Plot gating variable time constants as function of membrane potential.
    
        ax -- matplotlib axes to be plotted on
        parameters -- dictionary of parameters for gating variable time constant equations
        """
    
        tau_group = NeuronGroup(100,
                                Equations('v : volt') +
                                reduce(operator.add, [construct_gating_variable_tau_equation(
                                    gv) for gv in ['m', 'n', 'h']]),
                                method='euler', namespace=parameters)
    
        min_v = -100
        max_v = 100
        tau_group.v = np.linspace(min_v, max_v, len(tau_group))*mV
    
        ax.plot(tau_group.v/mV, tau_group.tau_m/ms, label=r'$\tau_m$')
        ax.plot(tau_group.v/mV, tau_group.tau_n/ms, label=r'$\tau_n$')
        ax.plot(tau_group.v/mV, tau_group.tau_h/ms, label=r'$\tau_h$')
    
        ax.set_xlabel('$v$ (mV)')
        ax.set_ylabel(r'$\tau$ (ms)')
        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()
        ax.legend()
    
    
    def plot_inf(ax, parameters):
        """Plot gating variable steady-state values as function of membrane potential.
    
        ax -- matplotlib axes to be plotted on
        parameters -- dictionary of parameters for gating variable steady-state equations
        """
    
        inf_group = NeuronGroup(100,
                                Equations('v : volt') +
                                reduce(operator.add, [construct_gating_variable_inf_equation(
                                    gv) for gv in ['m', 'n', 'h']]),
                                method='euler', namespace=parameters)
        inf_group.v = np.linspace(-100, 100, len(inf_group))*mV
    
        ax.plot(inf_group.v/mV, inf_group.m_inf, label=r'$m_\infty$')
        ax.plot(inf_group.v/mV, inf_group.n_inf, label=r'$n_\infty$')
        ax.plot(inf_group.v/mV, inf_group.h_inf, label=r'$h_\infty$')
        ax.set_xlabel('$v$ (mV)')
        ax.set_ylabel('steady-state activation')
        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()
        ax.legend()
    
    
    def plot_membrane_voltage(ax, statemon):
        """Plot simulation result: membrane potential.
    
        ax -- matplotlib axes to be plotted on
        statemon -- StateMonitor (with v recorded)
        """
    
        ax.plot(statemon.t/ms, statemon.v[0]/mV, label='membrane voltage')
        ax.set_xlabel('$t$ (ms)')
        ax.set_ylabel('$v$ (mV)')
        ax.axhline(0, linestyle='dashed')
        ax.legend()
    
    
    def plot_gating_variable_activations(ax, statemon):
        """Plot simulation result: gating variables.
    
        ax -- matplotlib axes to be plotted on
        statemon -- StateMonitor (with m, n and h recorded)
        """
    
        ax.plot(statemon.t/ms, statemon.m[0], label='$m$')
        ax.plot(statemon.t/ms, statemon.n[0], label='$n$')
        ax.plot(statemon.t/ms, statemon.h[0], label='$h$')
        ax.set_xlabel('$t$ (ms)')
        ax.set_ylabel('activation')
        ax.legend()
    
    
    def plot_conductances(ax, statemon):
        """Plot simulation result: conductances.
    
        ax -- matplotlib axes to be plotted on
        statemon -- StateMonitor (with g_K and g_Na recorded)
        """
    
        ax.plot(statemon.t/ms, statemon.g_K[0] / (mS/(cmeter**2)),
                label=r'$g_\mathregular{K}$')
    
        ax.plot(statemon.t/ms, statemon.g_Na[0] / (mS/(cmeter**2)),
                label=r'$g_\mathregular{Na}$')
    
        ax.set_xlabel('$t$ (ms)')
        ax.set_ylabel('$g$ (mS/cm$^2$)')
        ax.legend()
    
    
    def plot_currents(ax, statemon):
        """Plot simulation result: currents.
    
        ax -- matplotlib axes to be plotted on
        statemon -- StateMonitor (with I_K, I_Na and I_L recorded)
        """
    
        ax.plot(statemon.t/ms,
                statemon.I_K[0] / (uA/(cmeter**2)),
                label=r'$I_\mathregular{K}$')
    
        ax.plot(statemon.t/ms, statemon.I_Na[0] / (uA/(cmeter**2)),
                label=r'$I_\mathregular{Na}$')
    
        ax.plot(statemon.t/ms, (statemon.I_Na[0] + statemon.I_K[0] +
                                statemon.I_L[0]) / (uA/(cmeter**2)),
                label=r'$I_\mathregular{Na} + I_\mathregular{K} + I_\mathregular{L}$')
    
        ax.set_xlabel('$t$ (ms)')
        ax.set_ylabel(r'I ($\mu$A/cm$^2$)')
        ax.legend()
    
    
    def plot_current_stimulus(ax, statemon):
        """Plot simulation result: external current stimulus.
    
        ax -- matplotlib axes to be plotted on
        statemon -- StateMonitor (with I_ext recorded)
        """
    
        ax.plot(statemon.t/ms, statemon.I_ext[0] /
                (uA/(cmeter**2)), label=r'$I_\mathregular{ext}$')
    
        ax.set_xlabel('$t$ (ms)')
        ax.set_ylabel(r'I ($\mu$A/cm$^2$)')
        ax.legend()
    
    
    def plot_gating_variable_time_constants(ax, statemon):
        """Plot simulation result: gating variable time constants.
    
        ax -- matplotlib axes to be plotted on
        statemon -- StateMonitor (with tau_m, tau_n and tau_h recorded)
        """
    
        ax.plot(statemon.t/ms, statemon.tau_m[0]/ms, label=r'$\tau_m$')
        ax.plot(statemon.t/ms, statemon.tau_n[0]/ms, label=r'$\tau_n$')
        ax.plot(statemon.t/ms, statemon.tau_h[0]/ms, label=r'$\tau_h$')
    
        ax.set_xlabel('$t$ (ms)')
        ax.set_ylabel(r'$\tau$ (ms)')
        ax.legend()
    
    
    def run_simulation(parameters):
        """Run the simulation.
    
        parameters -- dictionary with parameters
        """
    
        equations = []
        for gating_variable in ["m", "n", "h"]:
            equations.append(
                construct_gating_variable_inf_equation(gating_variable))
            equations.append(
                construct_gating_variable_tau_equation(gating_variable))
            equations.append(construct_gating_variable_ode(gating_variable))
        equations += construct_neuron_ode()
    
        eqs_HH = reduce(operator.add, equations)
        group = NeuronGroup(1, eqs_HH, method='euler', namespace=parameters)
    
        group.v = parameters["v_initial"]
    
        group.m = parameters["m_initial"]
        group.n = parameters["n_initial"]
        group.h = parameters["h_initial"]
    
        statemon = StateMonitor(group, ['v',
                                        'I_ext',
                                        'm', 'n', 'h',
                                        'g_K', 'g_Na',
                                        'I_K', 'I_Na', 'I_L',
                                        'tau_m', 'tau_n', 'tau_h'],
                                record=True)
    
        defaultclock.dt = parameters["defaultclock_dt"]
        run(parameters["duration"])
    
        return statemon
    
    
    def main(parameters):
        """Run simulation and return matplotlib figure.
    
        parameters -- dictionary with parameters
        """
    
        statemon = run_simulation(parameters)
    
        fig = plt.figure(figsize=(20, 15), constrained_layout=True)
        gs = fig.add_gridspec(6, 2)
    
        ax0 = fig.add_subplot(gs[0, 0])
        ax1 = fig.add_subplot(gs[1, 0])
        ax2 = fig.add_subplot(gs[2, 0])
        ax3 = fig.add_subplot(gs[3, 0])
        ax4 = fig.add_subplot(gs[4, 0])
        ax5 = fig.add_subplot(gs[5, 0])
        ax6 = fig.add_subplot(gs[:3, 1])
        ax7 = fig.add_subplot(gs[3:, 1])
    
        plot_membrane_voltage(ax0, statemon)
        plot_gating_variable_activations(ax1, statemon)
        plot_conductances(ax2, statemon)
        plot_currents(ax3, statemon)
        plot_current_stimulus(ax4, statemon)
        plot_gating_variable_time_constants(ax5, statemon)
    
        plot_tau(ax6, parameters)
        plot_inf(ax7, parameters)
    
        return fig
    
    
    parameters = {
    
        # Boltzmann function parameters
        'v_n_half': 12*mV,
        'v_m_half': 25*mV,
        'v_h_half': 3*mV,
    
        'k_n': 15*mV,
        'k_m': 9*mV,
        'k_h': -7*mV,
    
        # Gaussian function parameters
        'v_n_max': -14*mV,
        'v_m_max': 27*mV,
        'v_h_max': -2*mV,
    
        'sigma_n': 50*mV,
        'sigma_m': 30*mV,
        'sigma_h': 20*mV,
    
        'c_n_amp': 4.7*ms,
        'c_m_amp': 0.46*ms,
        'c_h_amp': 7.4*ms,
    
        'c_n_base': 1.1*ms,
        'c_m_base': 0.04*ms,
        'c_h_base': 1.2*ms,
    
        # conductances
        'g_K_bar': 36*mS / (cmeter**2),
        'g_Na_bar': 120*mS / (cmeter**2),
        'g_L': 0.3*mS / (cmeter**2),
    
        # reversal potentials
        'e_K': -12*mV,
        'e_Na': 120*mV,
        'e_L': 10.6*mV,
    
        # membrane capacitance
        'C_mem': 1*uF / cmeter**2,
    
        # initial membrane voltage
        'v_initial': 0*mV,
    
        # initial gating variable activations
        'm_initial': 0.05,
        'n_initial': 0.32,
        'h_initial': 0.60,
    
        # external stimulus at 2 ms with 4 uA/cm^2 and at 10 ms with 15 uA/cm^2
        # for 0.5 ms each
        'I_stim': TimedArray(values=([0]*4+[4]+[0]*15+[15]+[0])*uA/(cmeter**2),
                             dt=0.5*ms),
    
        # simulation time step
        'defaultclock_dt': 0.01*ms,
    
        # simulation duration
        'duration': 20*ms
    }
    
    linestyle_cycler = cycler('linestyle',['-','--',':','-.'])
    plt.rc('axes', prop_cycle=linestyle_cycler)
    
    fig = main(parameters)
    
    plt.show()
    

![../_images/advanced.COBAHH_approximated.1.png](../_images/advanced.COBAHH_approximated.1.png)

---

# Example: CUBA2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/CUBA.html

# Example: CUBA

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/CUBA.ipynb)

This is a Brian script implementing a benchmark described in the following review paper:

Simulation of networks of spiking neurons: A review of tools and strategies (2007). Brette, Rudolph, Carnevale, Hines, Beeman, Bower, Diesmann, Goodman, Harris, Zirpe, Natschlager, Pecevski, Ermentrout, Djurfeldt, Lansner, Rochel, Vibert, Alvarez, Muller, Davison, El Boustani and Destexhe. Journal of Computational Neuroscience 23(3):349-98

Benchmark 2: random network of integrate-and-fire neurons with exponential synaptic currents.

Clock-driven implementation with exact subthreshold integration (but spike times are aligned to the grid).
    
    
    from brian2 import *
    
    taum = 20*ms
    taue = 5*ms
    taui = 10*ms
    Vt = -50*mV
    Vr = -60*mV
    El = -49*mV
    
    eqs = '''
    dv/dt  = (ge+gi-(v-El))/taum : volt (unless refractory)
    dge/dt = -ge/taue : volt
    dgi/dt = -gi/taui : volt
    '''
    
    P = NeuronGroup(4000, eqs, threshold='v>Vt', reset='v = Vr', refractory=5*ms,
                    method='exact')
    P.v = 'Vr + rand() * (Vt - Vr)'
    P.ge = 0*mV
    P.gi = 0*mV
    
    we = (60*0.27/10)*mV # excitatory synaptic weight (voltage)
    wi = (-20*4.5/10)*mV # inhibitory synaptic weight
    Ce = Synapses(P, P, on_pre='ge += we')
    Ci = Synapses(P, P, on_pre='gi += wi')
    Ce.connect('i<3200', p=0.02)
    Ci.connect('i>=3200', p=0.02)
    
    s_mon = SpikeMonitor(P)
    
    run(1 * second)
    
    plot(s_mon.t/ms, s_mon.i, ',k')
    xlabel('Time (ms)')
    ylabel('Neuron index')
    show()
    

![../_images/CUBA.1.png](../_images/CUBA.1.png)

---

# Example: IF_curve_Hodgkin_Huxley2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/IF_curve_Hodgkin_Huxley.html

# Example: IF_curve_Hodgkin_Huxley

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/IF_curve_Hodgkin_Huxley.ipynb)

Input-Frequency curve of a HH model.

Network: 100 unconnected Hodgin-Huxley neurons with an input current I. The input is set differently for each neuron.

This simulation should use exponential Euler integration.
    
    
    from brian2 import *
    
    num_neurons = 100
    duration = 2*second
    
    # Parameters
    area = 20000*umetre**2
    Cm = 1*ufarad*cm**-2 * area
    gl = 5e-5*siemens*cm**-2 * area
    El = -65*mV
    EK = -90*mV
    ENa = 50*mV
    g_na = 100*msiemens*cm**-2 * area
    g_kd = 30*msiemens*cm**-2 * area
    VT = -63*mV
    
    # The model
    eqs = Equations('''
    dv/dt = (gl*(El-v) - g_na*(m*m*m)*h*(v-ENa) - g_kd*(n*n*n*n)*(v-EK) + I)/Cm : volt
    dm/dt = 0.32*(mV**-1)*4*mV/exprel((13.*mV-v+VT)/(4*mV))/ms*(1-m)-0.28*(mV**-1)*5*mV/exprel((v-VT-40.*mV)/(5*mV))/ms*m : 1
    dn/dt = 0.032*(mV**-1)*5*mV/exprel((15.*mV-v+VT)/(5*mV))/ms*(1.-n)-.5*exp((10.*mV-v+VT)/(40.*mV))/ms*n : 1
    dh/dt = 0.128*exp((17.*mV-v+VT)/(18.*mV))/ms*(1.-h)-4./(1+exp((40.*mV-v+VT)/(5.*mV)))/ms*h : 1
    I : amp
    ''')
    # Threshold and refractoriness are only used for spike counting
    group = NeuronGroup(num_neurons, eqs,
                        threshold='v > -40*mV',
                        refractory='v > -40*mV',
                        method='exponential_euler')
    group.v = El
    group.I = '0.7*nA * i / num_neurons'
    
    monitor = SpikeMonitor(group)
    
    run(duration)
    
    plot(group.I/nA, monitor.count / duration)
    xlabel('I (nA)')
    ylabel('Firing rate (sp/s)')
    show()
    

![../_images/IF_curve_Hodgkin_Huxley.1.png](../_images/IF_curve_Hodgkin_Huxley.1.png)

---

# Example: IF_curve_LIF2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/IF_curve_LIF.html

# Example: IF_curve_LIF

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/IF_curve_LIF.ipynb)

Input-Frequency curve of a IF model.

Network: 1000 unconnected integrate-and-fire neurons (leaky IF) with an input parameter v0. The input is set differently for each neuron.
    
    
    from brian2 import *
    
    n = 1000
    duration = 1*second
    tau = 10*ms
    eqs = '''
    dv/dt = (v0 - v) / tau : volt (unless refractory)
    v0 : volt
    '''
    group = NeuronGroup(n, eqs, threshold='v > 10*mV', reset='v = 0*mV',
                        refractory=5*ms, method='exact')
    group.v = 0*mV
    group.v0 = '20*mV * i / (n-1)'
    
    monitor = SpikeMonitor(group)
    
    run(duration)
    plot(group.v0/mV, monitor.count / duration)
    xlabel('v0 (mV)')
    ylabel('Firing rate (sp/s)')
    show()
    

![../_images/IF_curve_LIF.1.png](../_images/IF_curve_LIF.1.png)

---

# Example: Ornstein_Uhlenbeck2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/advanced.Ornstein_Uhlenbeck.html

# Example: Ornstein_Uhlenbeck

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/advanced/Ornstein_Uhlenbeck.ipynb)

Ornstein-Uhlenbeck process

Figure 2: Two realizations of the Ornstein-Uhlenbeck process for parameters τ=1.0 and σ=0.1 (black curve), and for τ=0.1 and σ=0.31622 (red curve). In both cases the noise intensity is σ^2*τ=0.01 . The red curve represents a noise that more closely mimics Gaussian white noise. Both realizations begin here at x(0)=1.0 , after which the mean decays exponentially to zero with time constant τ.

Andre Longtin (2010) Stochastic dynamical systems. Scholarpedia, 5(4):1619.

Sebastian Schmitt, 2022
    
    
    import matplotlib.pyplot as plt
    import numpy as np
    
    from brian2 import run
    from brian2 import NeuronGroup, StateMonitor
    from brian2 import second, ms
    
    N = NeuronGroup(
        2,
        """
        tau : second
        sigma : 1
        dy/dt = -y/tau + sqrt(2*sigma**2/tau)*xi : 1
        """,
        method="euler"
    )
    
    N.tau = np.array([1, 0.1]) * second
    N.sigma = np.array([0.1, 0.31622])
    N.y = 1
    
    M = StateMonitor(N, "y", record=True)
    
    run(10 * second)
    
    plt.plot(M.t / second, M.y[1], color="red", label=r"$\tau$=0.1 s, $\sigma$=0.31622")
    plt.plot(M.t / second, M.y[0], color="k", label=r"$\tau$=1 s, $\sigma$=0.1")
    
    plt.xlim(0, 10)
    plt.ylim(-1.1, 1.1)
    
    plt.xlabel("time (sec)")
    plt.ylabel("Ornstein-Uhlenbeck process")
    
    plt.legend()
    
    plt.show()
    

![../_images/advanced.Ornstein_Uhlenbeck.1.png](../_images/advanced.Ornstein_Uhlenbeck.1.png)

---

# Example: STDP2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/synapses.STDP.html

# Example: STDP

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/synapses/STDP.ipynb)

Spike-timing dependent plasticity

Adapted from Song, Miller and Abbott (2000) and Song and Abbott (2001)
    
    
    from brian2 import *
    
    N = 1000
    taum = 10*ms
    taupre = 20*ms
    taupost = taupre
    Ee = 0*mV
    vt = -54*mV
    vr = -60*mV
    El = -74*mV
    taue = 5*ms
    F = 15*Hz
    gmax = .01
    dApre = .01
    dApost = -dApre * taupre / taupost * 1.05
    dApost *= gmax
    dApre *= gmax
    
    eqs_neurons = '''
    dv/dt = (ge * (Ee-v) + El - v) / taum : volt
    dge/dt = -ge / taue : 1
    '''
    
    poisson_input = PoissonGroup(N, rates=F)
    neurons = NeuronGroup(1, eqs_neurons, threshold='v>vt', reset='v = vr',
                          method='euler')
    S = Synapses(poisson_input, neurons,
                 '''w : 1
                    dApre/dt = -Apre / taupre : 1 (event-driven)
                    dApost/dt = -Apost / taupost : 1 (event-driven)''',
                 on_pre='''ge += w
                        Apre += dApre
                        w = clip(w + Apost, 0, gmax)''',
                 on_post='''Apost += dApost
                         w = clip(w + Apre, 0, gmax)''',
                 )
    S.connect()
    S.w = 'rand() * gmax'
    mon = StateMonitor(S, 'w', record=[0, 1])
    s_mon = SpikeMonitor(poisson_input)
    
    run(100*second, report='text')
    
    subplot(311)
    plot(S.w / gmax, '.k')
    ylabel('Weight / gmax')
    xlabel('Synapse index')
    subplot(312)
    hist(S.w / gmax, 20)
    xlabel('Weight / gmax')
    subplot(313)
    plot(mon.t/second, mon.w.T/gmax)
    xlabel('Time (s)')
    ylabel('Weight / gmax')
    tight_layout()
    show()
    

![../_images/synapses.STDP.1.png](../_images/synapses.STDP.1.png)

---

# Example: STDP_standalone2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/standalone.STDP_standalone.html

# Example: STDP_standalone

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/standalone/STDP_standalone.ipynb)

Spike-timing dependent plasticity. Adapted from Song, Miller and Abbott (2000) and Song and Abbott (2001).

This example is modified from `synapses_STDP.py` and writes a standalone C++ project in the directory `STDP_standalone`.
    
    
    from brian2 import *
    
    set_device('cpp_standalone', directory='STDP_standalone')
    
    N = 1000
    taum = 10*ms
    taupre = 20*ms
    taupost = taupre
    Ee = 0*mV
    vt = -54*mV
    vr = -60*mV
    El = -74*mV
    taue = 5*ms
    F = 15*Hz
    gmax = .01
    dApre = .01
    dApost = -dApre * taupre / taupost * 1.05
    dApost *= gmax
    dApre *= gmax
    
    eqs_neurons = '''
    dv/dt = (ge * (Ee-v) + El - v) / taum : volt
    dge/dt = -ge / taue : 1
    '''
    
    input = PoissonGroup(N, rates=F)
    neurons = NeuronGroup(1, eqs_neurons, threshold='v>vt', reset='v = vr',
                          method='euler')
    S = Synapses(input, neurons,
                 '''w : 1
                    dApre/dt = -Apre / taupre : 1 (event-driven)
                    dApost/dt = -Apost / taupost : 1 (event-driven)''',
                 on_pre='''ge += w
                        Apre += dApre
                        w = clip(w + Apost, 0, gmax)''',
                 on_post='''Apost += dApost
                         w = clip(w + Apre, 0, gmax)''',
                 )
    S.connect()
    S.w = 'rand() * gmax'
    mon = StateMonitor(S, 'w', record=[0, 1])
    s_mon = SpikeMonitor(input)
    
    run(100*second, report='text')
    
    subplot(311)
    plot(S.w / gmax, '.k')
    ylabel('Weight / gmax')
    xlabel('Synapse index')
    subplot(312)
    hist(S.w / gmax, 20)
    xlabel('Weight / gmax')
    subplot(313)
    plot(mon.t/second, mon.w.T/gmax)
    xlabel('Time (s)')
    ylabel('Weight / gmax')
    tight_layout()
    show()
    

![../_images/standalone.STDP_standalone.1.png](../_images/standalone.STDP_standalone.1.png)

---

# Example: adaptive_threshold2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/adaptive_threshold.html

# Example: adaptive_threshold

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/adaptive_threshold.ipynb)

A model with adaptive threshold (increases with each spike)
    
    
    from brian2 import *
    
    eqs = '''
    dv/dt = -v/(10*ms) : volt
    dvt/dt = (10*mV-vt)/(15*ms) : volt
    '''
    
    reset = '''
    v = 0*mV
    vt += 3*mV
    '''
    
    IF = NeuronGroup(1, model=eqs, reset=reset, threshold='v>vt',
                     method='exact')
    IF.vt = 10*mV
    PG = PoissonGroup(1, 500 * Hz)
    
    C = Synapses(PG, IF, on_pre='v += 3*mV')
    C.connect()
    
    Mv = StateMonitor(IF, 'v', record=True)
    Mvt = StateMonitor(IF, 'vt', record=True)
    # Record the value of v when the threshold is crossed
    M_crossings = SpikeMonitor(IF, variables='v')
    run(2*second, report='text')
    
    subplot(1, 2, 1)
    plot(Mv.t / ms, Mv[0].v / mV)
    plot(Mvt.t / ms, Mvt[0].vt / mV)
    ylabel('v (mV)')
    xlabel('t (ms)')
    # zoom in on the first 100ms
    xlim(0, 100)
    subplot(1, 2, 2)
    hist(M_crossings.v / mV, bins=np.arange(10, 20, 0.5))
    xlabel('v at threshold crossing (mV)')
    show()
    

![../_images/adaptive_threshold.1.png](../_images/adaptive_threshold.1.png)

---

# Example: bipolar_cell2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/compartmental.bipolar_cell.html

# Example: bipolar_cell

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/compartmental/bipolar_cell.ipynb)

A pseudo MSO neuron, with two dendrites and one axon (fake geometry).
    
    
    from brian2 import *
    
    # Morphology
    morpho = Soma(30*um)
    morpho.axon = Cylinder(diameter=1*um, length=300*um, n=100)
    morpho.L = Cylinder(diameter=1*um, length=100*um, n=50)
    morpho.R = Cylinder(diameter=1*um, length=150*um, n=50)
    
    # Passive channels
    gL = 1e-4*siemens/cm**2
    EL = -70*mV
    eqs='''
    Im = gL * (EL - v) : amp/meter**2
    I : amp (point current)
    '''
    
    neuron = SpatialNeuron(morphology=morpho, model=eqs,
                           Cm=1*uF/cm**2, Ri=100*ohm*cm, method='exponential_euler')
    neuron.v = EL
    neuron.I = 0*amp
    
    # Monitors
    mon_soma = StateMonitor(neuron, 'v', record=[0])
    mon_L = StateMonitor(neuron.L, 'v', record=True)
    mon_R = StateMonitor(neuron, 'v', record=morpho.R[75*um])
    
    run(1*ms)
    neuron.I[morpho.L[50*um]] = 0.2*nA  # injecting in the left dendrite
    run(5*ms)
    neuron.I = 0*amp
    run(50*ms, report='text')
    
    subplot(211)
    plot(mon_L.t/ms, mon_soma[0].v/mV, 'k')
    plot(mon_L.t/ms, mon_L[morpho.L[50*um]].v/mV, 'r')
    plot(mon_L.t/ms, mon_R[morpho.R[75*um]].v/mV, 'b')
    ylabel('v (mV)')
    subplot(212)
    for x in linspace(0*um, 100*um, 10, endpoint=False):
        plot(mon_L.t/ms, mon_L[morpho.L[x]].v/mV)
    xlabel('Time (ms)')
    ylabel('v (mV)')
    show()
    

![../_images/compartmental.bipolar_cell.1.png](../_images/compartmental.bipolar_cell.1.png)

---

# Example: bipolar_with_inputs2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/compartmental.bipolar_with_inputs.html

# Example: bipolar_with_inputs

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/compartmental/bipolar_with_inputs.ipynb)

A pseudo MSO neuron, with two dendrites (fake geometry). There are synaptic inputs.
    
    
    from brian2 import *
    
    # Morphology
    morpho = Soma(30*um)
    morpho.L = Cylinder(diameter=1*um, length=100*um, n=50)
    morpho.R = Cylinder(diameter=1*um, length=100*um, n=50)
    
    # Passive channels
    gL = 1e-4*siemens/cm**2
    EL = -70*mV
    Es = 0*mV
    eqs='''
    Im = gL*(EL-v) : amp/meter**2
    Is = gs*(Es-v) : amp (point current)
    gs : siemens
    '''
    
    neuron = SpatialNeuron(morphology=morpho, model=eqs,
                           Cm=1*uF/cm**2, Ri=100*ohm*cm, method='exponential_euler')
    neuron.v = EL
    
    # Regular inputs
    stimulation = NeuronGroup(2, 'dx/dt = 300*Hz : 1', threshold='x>1', reset='x=0',
                              method='euler')
    stimulation.x = [0, 0.5]  # Asynchronous
    
    # Synapses
    taus = 1*ms
    w = 20*nS
    S = Synapses(stimulation, neuron, model='''dg/dt = -g/taus : siemens (clock-driven)
                                               gs_post = g : siemens (summed)''',
                 on_pre='g += w', method='exact')
    
    S.connect(i=0, j=morpho.L[-1])
    S.connect(i=1, j=morpho.R[-1])
    
    # Monitors
    mon_soma = StateMonitor(neuron, 'v', record=[0])
    mon_L = StateMonitor(neuron.L, 'v', record=True)
    mon_R = StateMonitor(neuron.R, 'v',
                         record=morpho.R[-1])
    
    run(50*ms, report='text')
    
    subplot(211)
    plot(mon_L.t/ms, mon_soma[0].v/mV, 'k')
    plot(mon_L.t/ms, mon_L[morpho.L[-1]].v/mV, 'r')
    plot(mon_L.t/ms, mon_R[morpho.R[-1]].v/mV, 'b')
    ylabel('v (mV)')
    subplot(212)
    for x in linspace(0*um, 100*um, 10, endpoint=False):
        plot(mon_L.t/ms, mon_L[morpho.L[x]].v/mV)
    xlabel('Time (ms)')
    ylabel('v (mV)')
    show()
    

![../_images/compartmental.bipolar_with_inputs.1.png](../_images/compartmental.bipolar_with_inputs.1.png)

---

# Example: bipolar_with_inputs22.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/compartmental.bipolar_with_inputs2.html

# Example: bipolar_with_inputs2

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/compartmental/bipolar_with_inputs2.ipynb)

A pseudo MSO neuron, with two dendrites (fake geometry). There are synaptic inputs.

Second method.
    
    
    from brian2 import *
    
    # Morphology
    morpho = Soma(30*um)
    morpho.L = Cylinder(diameter=1*um, length=100*um, n=50)
    morpho.R = Cylinder(diameter=1*um, length=100*um, n=50)
    
    # Passive channels
    gL = 1e-4*siemens/cm**2
    EL = -70*mV
    Es = 0*mV
    taus = 1*ms
    eqs='''
    Im = gL*(EL-v) : amp/meter**2
    Is = gs*(Es-v) : amp (point current)
    dgs/dt = -gs/taus : siemens
    '''
    
    neuron = SpatialNeuron(morphology=morpho, model=eqs,
                           Cm=1*uF/cm**2, Ri=100*ohm*cm, method='exponential_euler')
    neuron.v = EL
    
    # Regular inputs
    stimulation = NeuronGroup(2, 'dx/dt = 300*Hz : 1', threshold='x>1', reset='x=0',
                              method='euler')
    stimulation.x = [0, 0.5] # Asynchronous
    
    # Synapses
    w = 20*nS
    S = Synapses(stimulation, neuron, on_pre='gs += w')
    S.connect(i=0, j=morpho.L[99.9*um])
    S.connect(i=1, j=morpho.R[99.9*um])
    
    # Monitors
    mon_soma = StateMonitor(neuron, 'v', record=[0])
    mon_L = StateMonitor(neuron.L, 'v', record=True)
    mon_R = StateMonitor(neuron, 'v', record=morpho.R[99.9*um])
    
    run(50*ms, report='text')
    
    subplot(211)
    plot(mon_L.t/ms, mon_soma[0].v/mV, 'k')
    plot(mon_L.t/ms, mon_L[morpho.L[99.9*um]].v/mV, 'r')
    plot(mon_L.t/ms, mon_R[morpho.R[99.9*um]].v/mV, 'b')
    ylabel('v (mV)')
    subplot(212)
    for i in [0, 5, 10, 15, 20, 25, 30, 35, 40, 45]:
        plot(mon_L.t/ms, mon_L.v[i, :]/mV)
    xlabel('Time (ms)')
    ylabel('v (mV)')
    show()
    

![../_images/compartmental.bipolar_with_inputs2.1.png](../_images/compartmental.bipolar_with_inputs2.1.png)

---

# Example: compare_GSL_to_conventional2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/advanced.compare_GSL_to_conventional.html

# Example: compare_GSL_to_conventional

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/advanced/compare_GSL_to_conventional.ipynb)

Example using GSL ODE solvers with a variable time step and comparing it to the Brian solver.

For highly accurate simulations, i.e. simulations with a very low desired error, the GSL simulation with a variable time step can be faster because it uses a low time step only when it is necessary. In biologically detailed models (e.g. of the Hodgkin-Huxley type), the relevant time constants are very short around an action potential, but much longer when the neuron is near its resting potential. The following example uses a very simple neuron model (leaky integrate-and-fire), but simulates a change in relevant time constants by changing the actual time constant every 10ms, independently for each of 100 neurons. To accurately simulate this model with a fixed time step, the time step has to be very small, wasting many unnecessary steps for all the neurons where the time constant is long.

Note that using the GSL ODE solver is much slower, if both methods use a comparable number of steps, i.e. if the desired accuracy is low enough so that a single step per “Brian time step” is enough.
    
    
    from brian2 import *
    import time
    
    # Run settings
    start_dt = .1 * ms
    method = 'rk2'
    error = 1.e-6  # requested accuracy
    
    
    def runner(method, dt, options=None):
        seed(0)
        I = 5
        group = NeuronGroup(100, '''dv/dt = (-v + I)/tau : 1
                                    tau : second''',
                            method=method,
                            method_options=options,
                            dt=dt)
        group.run_regularly('''v = rand()
                               tau = 0.1*ms + rand()*9.9*ms''', dt=10*ms)
    
        rec_vars = ['v', 'tau']
        if 'gsl' in method:
            rec_vars += ['_step_count']
        net = Network(group)
        net.run(0 * ms)
        mon = StateMonitor(group, rec_vars, record=True, dt=start_dt)
        net.add(mon)
        start = time.time()
        net.run(1 * second)
        mon.add_attribute('run_time')
        mon.run_time = time.time() - start
        return mon
    
    
    lin = runner('linear', start_dt)
    method_options = {'save_step_count': True,
                      'absolute_error': error,
                      'max_steps': 10000}
    gsl = runner('gsl_%s' % method, start_dt, options=method_options)
    
    print("Running with GSL integrator and variable time step:")
    print('Run time: %.3fs' % gsl.run_time)
    
    # check gsl error
    assert np.max(np.abs(
        lin.v - gsl.v)) < error, "Maximum error gsl integration too large: %f" % np.max(
        np.abs(lin.v - gsl.v))
    print("average step count: %.1f" % np.mean(gsl._step_count))
    print("average absolute error: %g" % np.mean(np.abs(gsl.v - lin.v)))
    
    print("\nRunning with exact integration and fixed time step:")
    dt = start_dt
    count = 0
    dts = []
    avg_errors = []
    max_errors = []
    runtimes = []
    while True:
        print('Using dt: %s' % str(dt))
        brian = runner(method, dt)
        print('\tRun time: %.3fs' % brian.run_time)
        avg_errors.append(np.mean(np.abs(brian.v - lin.v)))
        max_errors.append(np.max(np.abs(brian.v - lin.v)))
        dts.append(dt)
        runtimes.append(brian.run_time)
        if np.max(np.abs(brian.v - lin.v)) > error:
            print('\tError too high (%g), decreasing dt' % np.max(
                np.abs(brian.v - lin.v)))
            dt *= .5
            count += 1
        else:
            break
    print("Desired error level achieved:")
    print("average step count: %.2fs" % (start_dt / dt))
    print("average absolute error: %g" % np.mean(np.abs(brian.v - lin.v)))
    
    print('Run time: %.3fs' % brian.run_time)
    if brian.run_time > gsl.run_time:
        print("This is %.1f times slower than the simulation with GSL's variable "
              "time step method." % (brian.run_time / gsl.run_time))
    else:
        print("This is %.1f times faster than the simulation with GSL's variable "
              "time step method." % (gsl.run_time / brian.run_time))
    
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax2.axvline(1e-6, color='gray')
    for label, gsl_error, std_errors, ax in [('average absolute error', np.mean(np.abs(gsl.v - lin.v)), avg_errors, ax1),
                                             ('maximum absolute error', np.max(np.abs(gsl.v - lin.v)), max_errors, ax2)]:
        ax.set(xscale='log', yscale='log')
        ax.plot([], [], 'o', color='C0', label='fixed time step')  # for the legend entry
        for (error, runtime, dt) in zip(std_errors, runtimes, dts):
            ax.plot(error, runtime, 'o', color='C0')
            ax.annotate('%s' % str(dt), xy=(error, runtime), xytext=(2.5, 5),
                        textcoords='offset points', color='C0')
        ax.plot(gsl_error, gsl.run_time, 'o', color='C1', label='variable time step (GSL)')
        ax.set(xlabel=label, xlim=(10**-10, 10**1))
    ax1.set_ylabel('runtime (s)')
    ax2.legend(loc='lower left')
    
    plt.show()
    

![../_images/advanced.compare_GSL_to_conventional.1.png](../_images/advanced.compare_GSL_to_conventional.1.png)

---

# Example: continuous_interaction2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/synapses.continuous_interaction.html

# Example: continuous_interaction

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/synapses/continuous_interaction.ipynb)

## Synaptic model with continuous interaction

This example implements a conductance base synapse that is continuously linking two neurons, i.e. the synaptic gating variable updates at each time step. Two Reduced Traub-Miles Model (RTM) neurons are connected to each other through a directed synapse from neuron 1 to 2.

Here, the complexity stems from the fact that the synaptic conductance is a continuous function of the membrane potential, instead of being triggered by individual spikes. This can be useful in particular when analyzing models mathematically but it is not recommended in most cases because they tend to be less efficient. Also note that this model only works with (pre-synaptic) neuron models that model the action potential in detail, i.e. not with integrate-and-fire type models.

There are two broad approaches (`s` as part of the pre-synaptic neuron or `s` as part of the Synapses object), all depends on whether the time constants are the same across all synapses or whether they can vary between synapses. In this example, the time constant is assumed to be the same and `s` is therefore part of the pre-synaptic neuron model.

References:

  * Introduction to modeling neural dynamics, Börgers, chapter 20

  * [Discussion in Brian forum](https://brian.discourse.group/t/how-to-implement-a-conductance-base-synapse/77/2)

    
    
    from brian2 import *
    
    I_e = 1.5*uA
    simulation_time = 100*ms
    # neuron RTM parameters
    El = -67 * mV
    EK = -100 * mV
    ENa = 50 * mV
    ESyn = 0 * mV
    gl = 0.1 * msiemens
    gK = 80 * msiemens
    gNa = 100 * msiemens
    
    C = 1 * ufarad
    
    weight = 0.25
    gSyn = 1.0 * msiemens
    tau_d = 2 * ms
    tau_r = 0.2 * ms
    
    # forming RTM model with differential equations
    eqs = """
    alphah = 0.128 * exp(-(vm + 50.0*mV) / (18.0*mV))/ms :Hz
    alpham = 0.32/mV * (vm + 54*mV) / (1.0 - exp(-(vm + 54.0*mV) / (4.0*mV)))/ms:Hz
    alphan = 0.032/mV * (vm + 52*mV) / (1.0 - exp(-(vm + 52.0*mV) / (5.0*mV)))/ms:Hz
    
    betah  = 4.0 / (1.0 + exp(-(vm + 27.0*mV) / (5.0*mV)))/ms:Hz
    betam  = 0.28/mV * (vm + 27.0*mV) / (exp((vm + 27.0*mV) / (5.0*mV)) - 1.0)/ms:Hz
    betan  = 0.5 * exp(-(vm + 57.0*mV) / (40.0*mV))/ms:Hz
    
    membrane_Im = I_ext + gNa*m**3*h*(ENa-vm) +
                  gl*(El-vm) + gK*n**4*(EK-vm) + gSyn*s_in*(-vm): amp
    I_ext : amp
    s_in  : 1
    
    dm/dt = alpham*(1-m)-betam*m : 1
    dn/dt = alphan*(1-n)-betan*n : 1
    dh/dt = alphah*(1-h)-betah*h : 1
    
    ds/dt = 0.5 * (1 + tanh(0.1*vm/mV)) * (1-s)/tau_r - s/tau_d : 1
    
    dvm/dt = membrane_Im/C : volt
    """
    
    neuron = NeuronGroup(2, eqs, method="exponential_euler")
    
    # initialize variables
    neuron.vm = [-70.0, -65.0]*mV
    neuron.m = "alpham / (alpham + betam)"
    neuron.h = "alphah / (alphah + betah)"
    neuron.n = "alphan / (alphan + betan)"
    neuron.I_ext = [I_e, 0.0*uA]
    
    S = Synapses(neuron,
                 neuron,
                 's_in_post = weight*s_pre:1 (summed)')
    S.connect(i=0, j=1)
    
    # tracking variables
    st_mon = StateMonitor(neuron, ["vm", "s", "s_in"], record=[0, 1])
    
    # running the simulation
    run(simulation_time)
    
    # plot the results
    fig, ax = plt.subplots(2, figsize=(10, 6), sharex=True,
                           gridspec_kw={'height_ratios': (3, 1)})
    
    ax[0].plot(st_mon.t/ms, st_mon.vm[0]/mV,
               lw=2, c="r", alpha=0.5, label="neuron 0")
    ax[0].plot(st_mon.t/ms, st_mon.vm[1]/mV,
               lw=2, c="b", alpha=0.5, label='neuron 1')
    ax[1].plot(st_mon.t/ms, st_mon.s[0],
               lw=2, c="r", alpha=0.5, label='s, neuron 0')
    ax[1].plot(st_mon.t/ms, st_mon.s_in[1],
               lw=2, c="b", alpha=0.5, label='s_in, neuron 1')
    ax[0].set(ylabel='v [mV]', xlim=(0, np.max(st_mon.t / ms)),
              ylim=(-100, 50))
    ax[1].set(xlabel="t [ms]", ylabel="s", ylim=(0, 1))
    
    ax[0].legend()
    ax[1].legend()
    
    plt.show()
    

![../_images/synapses.continuous_interaction.1.png](../_images/synapses.continuous_interaction.1.png)

---

# Example: coupled_oscillators2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/coupled_oscillators.html

# Example: coupled_oscillators

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/coupled_oscillators.ipynb)

Coupled oscillators, following the Kuramoto model. The current state of an oscillator is given by its phase \\(\Theta\\), which follows

\\[\frac{d\Theta_i}{dt} = \omega_i + \frac{K}{N}\sum_j sin(\Theta_j - \Theta_i)\\]

where \\(\omega_i\\) is the intrinsic frequency of each oscillator, \\(K\\) is the coupling strength, and the sum is over all oscillators (all-to-all coupling).

The plots show a dot on the unit circle denoting the phase of each neuron (with the color representing the initial phase at the start of the simulation). The black dot and line show the average phase (dot) and the phase coherence (length of the line). The simulations are run four times with different coupling strengths \\(K\\), each simulation starting from the same initial phase distribution.

<https://en.wikipedia.org/wiki/Kuramoto_model>
    
    
    import matplotlib.animation as animation
    
    from brian2 import *
    from brian2.core.functions import timestep
    
    ### global parameters
    N = 100
    defaultclock.dt = 1*ms
    
    
    ### simulation code
    def run_sim(K, random_seed=214040893):
        seed(random_seed)
    
        eqs = '''
        dTheta/dt = omega + K/N*coupling : radian
        omega : radian/second (constant) # intrinsic frequency
        coupling : 1
        '''
    
        oscillators = NeuronGroup(N, eqs, method='euler')
        oscillators.Theta = 'rand()*2*pi'  # random initial phase
        oscillators.omega = 'clip(0.5 + randn()*0.5, 0, inf)*radian/second'  # 𝒩(0.5, 0.5)
    
        connections = Synapses(oscillators, oscillators,
                            'coupling_post = sin(Theta_pre - Theta_post) : 1 (summed)')
        connections.connect()  # all-to-all
    
        mon = StateMonitor(oscillators, 'Theta', record=True)
        run(10*second)
        return mon.Theta[:]
    
    ### Create animated plots
    frame_delay = 40*ms
    
    # Helper functions
    def to_x_y(phases):
        return np.cos(phases), np.sin(phases)
    
    def calc_coherence_and_phase(x, y):
        phi = np.arctan2(np.sum(y), np.sum(x))
        r = np.sqrt(np.sum(x)**2 + np.sum(y)**2)/N
        return r, phi
    
    # Plot an animation with the phase of each oscillator and the average phase
    def do_animation(fig, axes, K_values, theta_values):
        '''
        Makes animated subplots in the given ``axes``, where each ``theta_values`` entry
        is the full recording of ``Theta`` from the monitor.
        '''
        artists = []
        for ax, K, Theta in zip(axes, K_values, theta_values):
            x, y = to_x_y(Theta.T[0])
            dots = ax.scatter(x, y, c=Theta.T[0])
            r, phi = calc_coherence_and_phase(x, y)
            arrow = ax.arrow(0, 0, r*np.cos(phi), r*np.sin(phi), color='black')
            mean_dot, = ax.plot(r*np.cos(phi), r*np.sin(phi), 'o', color='black')
            if abs(K) > 0:
                title = f"coupling strength K={K:.1f}"
            else:
                title = "uncoupled"
            ax.text(-1., 1.05, title, color='gray', va='bottom')
            ax.set_aspect('equal')
            ax.set_axis_off()
            ax.set(xlim=(-1.2, 1.2), ylim=(-1.2, 1.2))
            artists.append((dots, arrow, mean_dot))
    
    
        def update(frame_number):
            updated_artists = []
            for (dots, arrow, mean_dot), K, Theta in zip(artists, K_values, theta_values):
                t = frame_delay*frame_number
                ts = timestep(t, defaultclock.dt)
                x, y = to_x_y(Theta.T[ts])
                dots.set_offsets(np.vstack([x, y]).T)
                r, phi = calc_coherence_and_phase(x, y)
                arrow.set_data(dx=r*np.cos(phi), dy=r*np.sin(phi))
                mean_dot.set_data(r*np.cos(phi), r*np.sin(phi))
                updated_artists.extend([dots, arrow, mean_dot])
            return updated_artists
    
        ani = animation.FuncAnimation(fig, update, frames=int(magic_network.t/frame_delay),
                                    interval=20, blit=True)
    
        return ani
    
    if __name__ == '__main__':
        fig, axs = plt.subplots(2, 2)
        # Manual adjustments instead of layout='tight', to avoid jumps in saved animation
        fig.subplots_adjust(left=0.025, bottom=0.025, right=0.975,  top=0.975,
                            wspace=0, hspace=0)
        K_values = [0, 1, 2, 4]
        theta_values = []
        for K in K_values:
            print(f"Running simulation for K={K:.1f}")
            theta_values.append( run_sim(K/second))
        ani = do_animation(fig, axs.flat, K_values, theta_values)
    
        plt.show()
    

![../_images/coupled_oscillators.1.gif](../_images/coupled_oscillators.1.gif)

---

# Example: cuba_openmp2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/standalone.cuba_openmp.html

# Example: cuba_openmp

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/standalone/cuba_openmp.ipynb)

Run the `cuba.py` example with OpenMP threads.
    
    
    from brian2 import *
    
    set_device('cpp_standalone', directory='CUBA')
    prefs.devices.cpp_standalone.openmp_threads = 4
    
    taum = 20*ms
    taue = 5*ms
    taui = 10*ms
    Vt = -50*mV
    Vr = -60*mV
    El = -49*mV
    
    eqs = '''
    dv/dt  = (ge+gi-(v-El))/taum : volt (unless refractory)
    dge/dt = -ge/taue : volt (unless refractory)
    dgi/dt = -gi/taui : volt (unless refractory)
    '''
    
    P = NeuronGroup(4000, eqs, threshold='v>Vt', reset='v = Vr', refractory=5*ms,
                    method='exact')
    P.v = 'Vr + rand() * (Vt - Vr)'
    P.ge = 0*mV
    P.gi = 0*mV
    
    we = (60*0.27/10)*mV # excitatory synaptic weight (voltage)
    wi = (-20*4.5/10)*mV # inhibitory synaptic weight
    Ce = Synapses(P, P, on_pre='ge += we')
    Ci = Synapses(P, P, on_pre='gi += wi')
    Ce.connect('i<3200', p=0.02)
    Ci.connect('i>=3200', p=0.02)
    
    s_mon = SpikeMonitor(P)
    
    run(1 * second)
    
    plot(s_mon.t/ms, s_mon.i, ',k')
    xlabel('Time (ms)')
    ylabel('Neuron index')
    show()
    

![../_images/standalone.cuba_openmp.1.png](../_images/standalone.cuba_openmp.1.png)

---

# Example: custom_events2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/advanced.custom_events.html

# Example: custom_events

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/advanced/custom_events.ipynb)

Example demonstrating the use of custom events.

Here we have three neurons, the first is Poisson spiking and connects to neuron G, which in turn connects to neuron H. Neuron G has two variables v and g, and the incoming Poisson spikes cause an instantaneous increase in variable g. g decays rapidly, and in turn causes a slow increase in v. If v crosses a threshold, it causes a standard spike and reset. If g crosses a threshold, it causes a custom event `gspike`, and if it returns below that threshold it causes a custom event `end_gspike`. The standard spike event when v crosses a threshold causes an instantaneous increase in variable x in neuron H (which happens through the standard `pre` pathway in the synapses), and the gspike event causes an increase in variable y (which happens through the custom pathway `gpath`).
    
    
    from brian2 import *
    # Input Poisson spikes
    inp = PoissonGroup(1, rates=250*Hz)
    # First group G
    eqs_G = '''
    dv/dt = (g-v)/(50*ms) : 1
    dg/dt = -g/(10*ms) : 1
    allow_gspike : boolean
    '''
    G = NeuronGroup(1, eqs_G, threshold='v>1',
                    reset='v = 0; g = 0; allow_gspike = True;',
                    events={'gspike': 'g>1 and allow_gspike',
                            'end_gspike': 'g<1 and not allow_gspike'})
    G.run_on_event('gspike', 'allow_gspike = False')
    G.run_on_event('end_gspike', 'allow_gspike = True')
    # Second group H
    eqs_H = '''
    dx/dt = -x/(10*ms) : 1
    dy/dt = -y/(10*ms) : 1
    '''
    H = NeuronGroup(1, eqs_H)
    # Synapses from input Poisson group to G
    Sin = Synapses(inp, G, on_pre='g += 0.5')
    Sin.connect()
    # Synapses from G to H
    S = Synapses(G, H,
                 on_pre={'pre': 'x += 1',
                         'gpath': 'y += 1'},
                 on_event={'pre': 'spike',
                           'gpath': 'gspike'})
    S.connect()
    # Monitors
    Mstate = StateMonitor(G, ('v', 'g'), record=True)
    Mgspike = EventMonitor(G, 'gspike', 'g')
    Mspike = SpikeMonitor(G, 'v')
    MHstate = StateMonitor(H, ('x', 'y'), record=True)
    # Initialise and run
    G.allow_gspike = True
    run(500*ms)
    # Plot
    figure(figsize=(10, 4))
    subplot(121)
    plot(Mstate.t/ms, Mstate.g[0], '-g', label='g')
    plot(Mstate.t/ms, Mstate.v[0], '-b', lw=2, label='V')
    plot(Mspike.t/ms, Mspike.v, 'ob', label='_nolegend_')
    plot(Mgspike.t/ms, Mgspike.g, 'og', label='_nolegend_')
    xlabel('Time (ms)')
    title('Presynaptic group G')
    legend(loc='best')
    subplot(122)
    plot(MHstate.t/ms, MHstate.y[0], '-r', label='y')
    plot(MHstate.t/ms, MHstate.x[0], '-k', lw=2, label='x')
    xlabel('Time (ms)')
    title('Postsynaptic group H')
    legend(loc='best')
    tight_layout()
    show()
    

![../_images/advanced.custom_events.1.png](../_images/advanced.custom_events.1.png)

---

# Example: cylinder2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/compartmental.cylinder.html

# Example: cylinder

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/compartmental/cylinder.ipynb)

A short cylinder with constant injection at one end.
    
    
    from brian2 import *
    
    defaultclock.dt = 0.01*ms
    
    # Morphology
    diameter = 1*um
    length = 300*um
    Cm = 1*uF/cm**2
    Ri = 150*ohm*cm
    N = 200
    morpho = Cylinder(diameter=diameter, length=length, n=N)
    
    # Passive channels
    gL = 1e-4*siemens/cm**2
    EL = -70*mV
    eqs = '''
    Im = gL * (EL - v) : amp/meter**2
    I : amp (point current)
    '''
    
    neuron = SpatialNeuron(morphology=morpho, model=eqs, Cm=Cm, Ri=Ri,
                           method='exponential_euler')
    neuron.v = EL
    
    la = neuron.space_constant[0]
    print("Electrotonic length: %s" % la)
    
    neuron.I[0] = 0.02*nA # injecting at the left end
    run(100*ms, report='text')
    
    plot(neuron.distance/um, neuron.v/mV, 'kx')
    # Theory
    x = neuron.distance
    ra = la * 4 * Ri / (pi * diameter**2)
    theory = EL + ra * neuron.I[0] * cosh((length - x) / la) / sinh(length / la)
    plot(x/um, theory/mV, 'r')
    xlabel('x (um)')
    ylabel('v (mV)')
    show()
    

![../_images/compartmental.cylinder.1.png](../_images/compartmental.cylinder.1.png)

---

# Example: efficient_gaussian_connectivity2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/synapses.efficient_gaussian_connectivity.html

# Example: efficient_gaussian_connectivity

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/synapses/efficient_gaussian_connectivity.ipynb)

An example of turning an expensive [`Synapses.connect`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses.connect "brian2.synapses.synapses.Synapses.connect") operation into three cheap ones using a mathematical trick.

Consider the connection probability between neurons i and j given by the Gaussian function \\(p=e^{-\alpha(i-j)^2}\\) (for some constant \\(\alpha\\)). If we want to connect neurons with this probability, we can very simply do:
    
    
    S.connect(p='exp(-alpha*(i-j)**2)')
    

However, this has a problem. Although we know that this will create \\(O(N)\\) synapses if N is the number of neurons, because we have specified `p` as a function of i and j, we have to evaluate `p(i, j)` for every pair `(i, j)`, and therefore it takes \\(O(N^2)\\) operations.

Our first option is to take a cutoff, and say that if \\(p<q\\) for some small \\(q\\), then we assume that \\(p\approx 0\\). We can work out which j values are compatible with a given value of i by solving \\(e^{-\alpha(i-j)^2}<q\\) which gives \\(|i-j|<\sqrt{-\log(q)/\alpha)}=w\\). Now we implement the rule using the generator syntax to only search for values between `i-w` and `i+w`, except that some of these values will be outside the valid range of values for j so we set `skip_if_invalid=True`. The connection code is then:
    
    
    S.connect(j='k for k in range(i-w, i+w) if rand()<exp(-alpha*(i-j)**2)',
              skip_if_invalid=True)
    

This is a lot faster (see graph labelled “Limited” for this algorithm).

However, it may be a problem that we have to specify a cutoff and so we will lose some synapses doing this: it won’t be mathematically exact. This isn’t a problem for the Gaussian because w grows very slowly with the cutoff probability q, but for other probability distributions with more weight in the tails, it could be an issue.

If we want to be exact, we can still do a big improvement. For the case \\(i-w\leq j\leq i+w\\) we use the same connection code, but we also handle the case \\(|i-j|>w\\). This time, we note that we want to create a synapse with probability \\(p(i-j)\\) and we can rewrite this as \\(p(i-j)/p(w)\cdot p(w)\\). If \\(|i-j|>w\\) then this is a product of two probabilities \\(p(i-j)/p(w)\\) and \\(p(w)\\). So in the region \\(|i-j|>w\\) a synapse will be created if two random events both occur, with these two probabilities. This might seem a little strange until you notice that one of the two probabilities \\(p(w)\\) doesn’t depend on i or j. This lets us use the much more efficient `sample` algorithm to generate a set of candidate `j` values, and then add the additional test `rand()<p(i-j)/p(w)`. Here’s the code for that:
    
    
    w = int(ceil(sqrt(log(q)/-0.1)))
    S.connect(j='k for k in range(i-w, i+w) if rand()<exp(-alpha*(i-j)**2)',
              skip_if_invalid=True)
    pmax = exp(-0.1*w**2)
    S.connect(j='k for k in sample(0, i-w, p=pmax) if rand()<exp(-alpha*(i-j)**2)/pmax',
              skip_if_invalid=True)
    S.connect(j='k for k in sample(i+w, N_post, p=pmax) if rand()<exp(-alpha*(i-j)**2)/pmax',
              skip_if_invalid=True)
    

This “Divided” method is also much faster than the naive method, and is mathematically correct. Note though that this method is still \\(O(N^2)\\) but the constants are much, much smaller and this will usually be sufficient. It is possible to take the ideas developed here even further and get even better scaling, but in most cases it’s unlikely to be worth the effort.

The code below shows these examples written out, along with some timing code and plots for different values of N.
    
    
    from brian2 import *
    import time
    
    def naive(N):
        G = NeuronGroup(N, 'v:1', threshold='v>1', name='G')
        S = Synapses(G, G, on_pre='v += 1', name='S')
        S.connect(p='exp(-0.1*(i-j)**2)')
    
    def limited(N, q=0.001):
        G = NeuronGroup(N, 'v:1', threshold='v>1', name='G')
        S = Synapses(G, G, on_pre='v += 1', name='S')
        w = int(ceil(sqrt(log(q)/-0.1)))
        S.connect(j='k for k in range(i-w, i+w) if rand()<exp(-0.1*(i-j)**2)', skip_if_invalid=True)
    
    def divided(N, q=0.001):
        G = NeuronGroup(N, 'v:1', threshold='v>1', name='G')
        S = Synapses(G, G, on_pre='v += 1', name='S')
        w = int(ceil(sqrt(log(q)/-0.1)))
        S.connect(j='k for k in range(i-w, i+w) if rand()<exp(-0.1*(i-j)**2)', skip_if_invalid=True)
        pmax = exp(-0.1*w**2)
        S.connect(j='k for k in sample(0, i-w, p=pmax) if rand()<exp(-0.1*(i-j)**2)/pmax', skip_if_invalid=True)
        S.connect(j='k for k in sample(i+w, N_post, p=pmax) if rand()<exp(-0.1*(i-j)**2)/pmax', skip_if_invalid=True)
    
    def repeated_run(f, N, repeats):
        start_time = time.time()
        for _ in range(repeats):
            f(N)
        end_time = time.time()
        return (end_time-start_time)/repeats
    
    N = array([100, 500, 1000, 5000, 10000, 20000])
    repeats = array([100, 10, 10, 1, 1, 1])*3
    naive(10)
    limited(10)
    divided(10)
    print('Starting naive')
    loglog(N, [repeated_run(naive, n, r) for n, r in zip(N, repeats)],
           label='Naive', lw=2)
    print('Starting limit')
    loglog(N, [repeated_run(limited, n, r) for n, r in zip(N, repeats)],
           label='Limited', lw=2)
    print('Starting divided')
    loglog(N, [repeated_run(divided, n, r) for n, r in zip(N, repeats)],
           label='Divided', lw=2)
    xlabel('N')
    ylabel('Time (s)')
    legend(loc='best', frameon=False)
    show()
    

![../_images/synapses.efficient_gaussian_connectivity.1.png](../_images/synapses.efficient_gaussian_connectivity.1.png)

---

# Example: exprel_function2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/advanced.exprel_function.html

# Example: exprel_function

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/advanced/exprel_function.ipynb)

Show the improved numerical accuracy when using the `exprel()` function in rate equations.

Rate equations for channel opening/closing rates often include a term of the form \\(\frac{x}{\exp(x) - 1}\\). This term is problematic for two reasons:

  * It is not defined for \\(x = 0\\) (where it should equal to \\(1\\) for continuity);

  * For values \\(x \approx 0\\), there is a loss of accuracy.

For better accuracy, and to avoid issues at \\(x = 0\\), Brian provides the function `exprel()`, which is equivalent to \\(\frac{\exp(x) - 1}{x}\\), but with better accuracy and the expected result at \\(x = 0\\). In this example, we demonstrate the advantage of expressing a typical rate equation from the HH model with `exprel()`.
    
    
    from brian2 import *
    
    # Dummy group to evaluate the rate equation at various points
    eqs = '''v : volt
             # opening rate from the HH model
             alpha_simple = 0.32*(mV**-1)*(-50*mV-v)/
                            (exp((-50*mV-v)/(4*mV))-1.)/ms : Hz
             alpha_improved = 0.32*(mV**-1)*4*mV/exprel((-50*mV-v)/(4*mV))/ms : Hz'''
    neuron = NeuronGroup(1000, eqs)
    
    # Use voltage values around the problematic point
    neuron.v = np.linspace(-50 - .5e-6, -50 + .5e-6, len(neuron))*mV
    
    fig, ax = plt.subplots()
    ax.plot((neuron.v + 50*mV)/nvolt, neuron.alpha_simple,
             '.', label=r'$\alpha_\mathrm{simple}$')
    ax.plot((neuron.v + 50*mV)/nvolt, neuron.alpha_improved,
             'k', label=r'$\alpha_\mathrm{improved}$')
    ax.legend()
    ax.set(xlabel='$v$ relative to -50mV (nV)', ylabel=r'$\alpha$ (Hz)')
    ax.ticklabel_format(useOffset=False)
    plt.tight_layout()
    plt.show()
    

![../_images/advanced.exprel_function.1.png](../_images/advanced.exprel_function.1.png)

---

# Example: float_32_64_benchmark2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/advanced.float_32_64_benchmark.html

# Example: float_32_64_benchmark

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/advanced/float_32_64_benchmark.ipynb)

Benchmark showing the performance of float32 versus float64.
    
    
    from brian2 import *
    from brian2.devices.device import reset_device, reinit_devices
    
    # CUBA benchmark
    def run_benchmark(name):
        if name=='CUBA':
    
            taum = 20*ms
            taue = 5*ms
            taui = 10*ms
            Vt = -50*mV
            Vr = -60*mV
            El = -49*mV
    
            eqs = '''
            dv/dt  = (ge+gi-(v-El))/taum : volt (unless refractory)
            dge/dt = -ge/taue : volt
            dgi/dt = -gi/taui : volt
            '''
    
            P = NeuronGroup(4000, eqs, threshold='v>Vt', reset='v = Vr', refractory=5*ms,
                            method='exact')
            P.v = 'Vr + rand() * (Vt - Vr)'
            P.ge = 0*mV
            P.gi = 0*mV
    
            we = (60*0.27/10)*mV # excitatory synaptic weight (voltage)
            wi = (-20*4.5/10)*mV # inhibitory synaptic weight
            Ce = Synapses(P, P, on_pre='ge += we')
            Ci = Synapses(P, P, on_pre='gi += wi')
            Ce.connect('i<3200', p=0.02)
            Ci.connect('i>=3200', p=0.02)
    
        elif name=='COBA':
    
            # Parameters
            area = 20000 * umetre ** 2
            Cm = (1 * ufarad * cm ** -2) * area
            gl = (5e-5 * siemens * cm ** -2) * area
    
            El = -60 * mV
            EK = -90 * mV
            ENa = 50 * mV
            g_na = (100 * msiemens * cm ** -2) * area
            g_kd = (30 * msiemens * cm ** -2) * area
            VT = -63 * mV
            # Time constants
            taue = 5 * ms
            taui = 10 * ms
            # Reversal potentials
            Ee = 0 * mV
            Ei = -80 * mV
            we = 6 * nS  # excitatory synaptic weight
            wi = 67 * nS  # inhibitory synaptic weight
    
            # The model
            eqs = Equations('''
            dv/dt = (gl*(El-v)+ge*(Ee-v)+gi*(Ei-v)-
                     g_na*(m*m*m)*h*(v-ENa)-
                     g_kd*(n*n*n*n)*(v-EK))/Cm : volt
            dm/dt = alpha_m*(1-m)-beta_m*m : 1
            dn/dt = alpha_n*(1-n)-beta_n*n : 1
            dh/dt = alpha_h*(1-h)-beta_h*h : 1
            dge/dt = -ge*(1./taue) : siemens
            dgi/dt = -gi*(1./taui) : siemens
            alpha_m = 0.32*(mV**-1)*4*mV/exprel((13*mV-v+VT)/(4*mV))/ms : Hz
            beta_m = 0.28*(mV**-1)*5*mV/exprel((v-VT-40*mV)/(5*mV))/ms : Hz
            alpha_h = 0.128*exp((17*mV-v+VT)/(18*mV))/ms : Hz
            beta_h = 4./(1+exp((40*mV-v+VT)/(5*mV)))/ms : Hz
            alpha_n = 0.032*(mV**-1)*5*mV/exprel((15*mV-v+VT)/(5*mV))/ms : Hz
            beta_n = .5*exp((10*mV-v+VT)/(40*mV))/ms : Hz
            ''')
    
            P = NeuronGroup(4000, model=eqs, threshold='v>-20*mV', refractory=3 * ms,
                            method='exponential_euler')
            Pe = P[:3200]
            Pi = P[3200:]
            Ce = Synapses(Pe, P, on_pre='ge+=we')
            Ci = Synapses(Pi, P, on_pre='gi+=wi')
            Ce.connect(p=0.02)
            Ci.connect(p=0.02)
    
            # Initialization
            P.v = 'El + (randn() * 5 - 5)*mV'
            P.ge = '(randn() * 1.5 + 4) * 10.*nS'
            P.gi = '(randn() * 12 + 20) * 10.*nS'
    
        run(1 * second, profile=True)
    
        return sum(t for name, t in magic_network.profiling_info)
    
    def generate_results(num_repeats):
        results = {}
    
        for name in ['CUBA', 'COBA']:
            for target in ['numpy', 'cython']:
                for dtype in [float32, float64]:
                    prefs.codegen.target = target
                    prefs.core.default_float_dtype = dtype
                    times = [run_benchmark(name) for repeat in range(num_repeats)]
                    results[name, target, dtype.__name__] = amin(times)
    
        for name in ['CUBA', 'COBA']:
            for dtype in [float32, float64]:
                times = []
                for _ in range(num_repeats):
                    reset_device()
                    reinit_devices()
                    set_device('cpp_standalone', directory=None, with_output=False)
                    prefs.core.default_float_dtype = dtype
                    times.append(run_benchmark(name))
                results[name, 'cpp_standalone', dtype.__name__] = amin(times)
    
        return results
    
    results = generate_results(3)
    
    bar_width = 0.9
    names = ['CUBA', 'COBA']
    targets = ['numpy', 'cython', 'cpp_standalone']
    precisions = ['float32', 'float64']
    
    figure(figsize=(8, 8))
    for j, name in enumerate(names):
        subplot(2, 2, 1+2*j)
        title(name)
        index = arange(len(targets))
        for i, precision in enumerate(precisions):
            bar(index+i*bar_width/len(precisions),
                [results[name, target, precision] for target in targets],
                bar_width/len(precisions), label=precision, align='edge')
        ylabel('Time (s)')
        if j:
            xticks(index+0.5*bar_width, targets, rotation=45)
        else:
            xticks(index+0.5*bar_width, ('',)*len(targets))
            legend(loc='best')
    
        subplot(2, 2, 2+2*j)
        index = arange(len(precisions))
        for i, target in enumerate(targets):
            bar(index+i*bar_width/len(targets),
                [results[name, target, precision] for precision in precisions],
                bar_width/len(targets), label=target, align='edge')
        ylabel('Time (s)')
        if j:
            xticks(index+0.5*bar_width, precisions, rotation=45)
        else:
            xticks(index+0.5*bar_width, ('',)*len(precisions))
            legend(loc='best')
    
    tight_layout()
    show()
    

---

# Example: gapjunctions2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/synapses.gapjunctions.html

# Example: gapjunctions

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/synapses/gapjunctions.ipynb)

Neurons with gap junctions.
    
    
    from brian2 import *
    
    n = 10
    v0 = 1.05
    tau = 10*ms
    
    eqs = '''
    dv/dt = (v0 - v + Igap) / tau : 1
    Igap : 1 # gap junction current
    '''
    
    neurons = NeuronGroup(n, eqs, threshold='v > 1', reset='v = 0',
                          method='exact')
    neurons.v = 'i * 1.0 / (n-1)'
    trace = StateMonitor(neurons, 'v', record=[0, 5])
    
    S = Synapses(neurons, neurons, '''
                 w : 1 # gap junction conductance
                 Igap_post = w * (v_pre - v_post) : 1 (summed)
                 ''')
    S.connect()
    S.w = .02
    
    run(500*ms)
    
    plot(trace.t/ms, trace[0].v)
    plot(trace.t/ms, trace[5].v)
    xlabel('Time (ms)')
    ylabel('v')
    show()
    

![../_images/synapses.gapjunctions.1.png](../_images/synapses.gapjunctions.1.png)

---

# Example: hh_with_spikes2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/compartmental.hh_with_spikes.html

# Example: hh_with_spikes

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/compartmental/hh_with_spikes.ipynb)

Hodgkin-Huxley equations (1952).

Spikes are recorded along the axon, and then velocity is calculated.
    
    
    from brian2 import *
    from scipy import stats
    
    defaultclock.dt = 0.01*ms
    
    morpho = Cylinder(length=10*cm, diameter=2*238*um, n=1000, type='axon')
    
    El = 10.613*mV
    ENa = 115*mV
    EK = -12*mV
    gl = 0.3*msiemens/cm**2
    gNa0 = 120*msiemens/cm**2
    gK = 36*msiemens/cm**2
    
    # Typical equations
    eqs = '''
    # The same equations for the whole neuron, but possibly different parameter values
    # distributed transmembrane current
    Im = gl * (El-v) + gNa * m**3 * h * (ENa-v) + gK * n**4 * (EK-v) : amp/meter**2
    I : amp (point current) # applied current
    dm/dt = alpham * (1-m) - betam * m : 1
    dn/dt = alphan * (1-n) - betan * n : 1
    dh/dt = alphah * (1-h) - betah * h : 1
    alpham = (0.1/mV) * 10*mV/exprel((-v+25*mV)/(10*mV))/ms : Hz
    betam = 4 * exp(-v/(18*mV))/ms : Hz
    alphah = 0.07 * exp(-v/(20*mV))/ms : Hz
    betah = 1/(exp((-v+30*mV) / (10*mV)) + 1)/ms : Hz
    alphan = (0.01/mV) * 10*mV/exprel((-v+10*mV)/(10*mV))/ms : Hz
    betan = 0.125*exp(-v/(80*mV))/ms : Hz
    gNa : siemens/meter**2
    '''
    
    neuron = SpatialNeuron(morphology=morpho, model=eqs, method="exponential_euler",
                           refractory="m > 0.4", threshold="m > 0.5",
                           Cm=1*uF/cm**2, Ri=35.4*ohm*cm)
    neuron.v = 0*mV
    neuron.h = 1
    neuron.m = 0
    neuron.n = .5
    neuron.I = 0*amp
    neuron.gNa = gNa0
    M = StateMonitor(neuron, 'v', record=True)
    spikes = SpikeMonitor(neuron)
    
    run(50*ms, report='text')
    neuron.I[0] = 1*uA # current injection at one end
    run(3*ms)
    neuron.I = 0*amp
    run(50*ms, report='text')
    
    # Calculation of velocity
    slope, intercept, r_value, p_value, std_err = stats.linregress(spikes.t/second,
                                                    neuron.distance[spikes.i]/meter)
    print("Velocity = %.2f m/s" % slope)
    
    subplot(211)
    for i in range(10):
        plot(M.t/ms, M.v.T[:, i*100]/mV)
    ylabel('v')
    subplot(212)
    plot(spikes.t/ms, spikes.i*neuron.length[0]/cm, '.k')
    plot(spikes.t/ms, (intercept+slope*(spikes.t/second))/cm, 'r')
    xlabel('Time (ms)')
    ylabel('Position (cm)')
    show()
    

![../_images/compartmental.hh_with_spikes.1.png](../_images/compartmental.hh_with_spikes.1.png)

---

# Example: hodgkin_huxley_19522.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/compartmental.hodgkin_huxley_1952.html

# Example: hodgkin_huxley_1952

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/compartmental/hodgkin_huxley_1952.ipynb)

Hodgkin-Huxley equations (1952).
    
    
    from brian2 import *
    
    morpho = Cylinder(length=10*cm, diameter=2*238*um, n=1000, type='axon')
    
    El = 10.613*mV
    ENa = 115*mV
    EK = -12*mV
    gl = 0.3*msiemens/cm**2
    gNa0 = 120*msiemens/cm**2
    gK = 36*msiemens/cm**2
    
    # Typical equations
    eqs = '''
    # The same equations for the whole neuron, but possibly different parameter values
    # distributed transmembrane current
    Im = gl * (El-v) + gNa * m**3 * h * (ENa-v) + gK * n**4 * (EK-v) : amp/meter**2
    I : amp (point current) # applied current
    dm/dt = alpham * (1-m) - betam * m : 1
    dn/dt = alphan * (1-n) - betan * n : 1
    dh/dt = alphah * (1-h) - betah * h : 1
    alpham = (0.1/mV) * 10*mV/exprel((-v+25*mV)/(10*mV))/ms : Hz
    betam = 4 * exp(-v/(18*mV))/ms : Hz
    alphah = 0.07 * exp(-v/(20*mV))/ms : Hz
    betah = 1/(exp((-v+30*mV) / (10*mV)) + 1)/ms : Hz
    alphan = (0.01/mV) * 10*mV/exprel((-v+10*mV)/(10*mV))/ms : Hz
    betan = 0.125*exp(-v/(80*mV))/ms : Hz
    gNa : siemens/meter**2
    '''
    
    neuron = SpatialNeuron(morphology=morpho, model=eqs, Cm=1*uF/cm**2,
                           Ri=35.4*ohm*cm, method="exponential_euler")
    neuron.v = 0*mV
    neuron.h = 1
    neuron.m = 0
    neuron.n = .5
    neuron.I = 0
    neuron.gNa = gNa0
    neuron[5*cm:10*cm].gNa = 0*siemens/cm**2
    M = StateMonitor(neuron, 'v', record=True)
    
    run(50*ms, report='text')
    neuron.I[0] = 1*uA  # current injection at one end
    run(3*ms)
    neuron.I = 0*amp
    run(100*ms, report='text')
    for i in range(75, 125, 1):
        plot(cumsum(neuron.length)/cm, i+(1./60)*M.v[:, i*5]/mV, 'k')
    yticks([])
    ylabel('Time [major] v (mV) [minor]')
    xlabel('Position (cm)')
    axis('tight')
    show()
    

![../_images/compartmental.hodgkin_huxley_1952.1.png](../_images/compartmental.hodgkin_huxley_1952.1.png)

---

# Example: infinite_cable2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/compartmental.infinite_cable.html

# Example: infinite_cable

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/compartmental/infinite_cable.ipynb)

An (almost) infinite cable with pulse injection in the middle.
    
    
    from brian2 import *
    
    defaultclock.dt = 0.001*ms
    
    # Morphology
    diameter = 1*um
    Cm = 1*uF/cm**2
    Ri = 100*ohm*cm
    N = 500
    morpho = Cylinder(diameter=diameter, length=3*mm, n=N)
    
    # Passive channels
    gL = 1e-4*siemens/cm**2
    EL = -70*mV
    eqs = '''
    Im = gL * (EL-v) : amp/meter**2
    I : amp (point current)
    '''
    
    neuron = SpatialNeuron(morphology=morpho, model=eqs, Cm=Cm, Ri=Ri,
                           method = 'exponential_euler')
    neuron.v = EL
    
    taum = Cm  /gL  # membrane time constant
    print("Time constant: %s" % taum)
    la = neuron.space_constant[0]
    print("Characteristic length: %s" % la)
    
    # Monitors
    mon = StateMonitor(neuron, 'v', record=range(0, N//2, 20))
    
    neuron.I[len(neuron) // 2] = 1*nA  # injecting in the middle
    run(0.02*ms)
    neuron.I = 0*amp
    run(10*ms, report='text')
    
    t = mon.t
    plot(t/ms, mon.v.T/mV, 'k')
    # Theory (incorrect near cable ends)
    for i in range(0, len(neuron)//2, 20):
        x = (len(neuron)/2 - i) * morpho.length[0]
        theory = (1/(la*Cm*pi*diameter) * sqrt(taum / (4*pi*(t + defaultclock.dt))) *
                  exp(-(t+defaultclock.dt)/taum -
                      taum / (4*(t+defaultclock.dt))*(x/la)**2))
        theory = EL + theory * 1*nA * 0.02*ms
        plot(t/ms, theory/mV, 'r')
    xlabel('Time (ms)')
    ylabel('v (mV')
    show()
    

![../_images/compartmental.infinite_cable.1.png](../_images/compartmental.infinite_cable.1.png)

---

# Example: jeffress2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/synapses.jeffress.html

# Example: jeffress

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/synapses/jeffress.ipynb)

Jeffress model, adapted with spiking neuron models. A sound source (white noise) is moving around the head. Delay differences between the two ears are used to determine the azimuth of the source. Delays are mapped to a neural place code using delay lines (each neuron receives input from both ears, with different delays).
    
    
    from brian2 import *
    
    defaultclock.dt = .02*ms
    
    # Sound
    sound = TimedArray(10 * randn(50000), dt=defaultclock.dt) # white noise
    
    # Ears and sound motion around the head (constant angular speed)
    sound_speed = 300*metre/second
    interaural_distance = 20*cm # big head!
    max_delay = interaural_distance / sound_speed
    print("Maximum interaural delay: %s" % max_delay)
    angular_speed = 2 * pi / second # 1 turn/second
    tau_ear = 1*ms
    sigma_ear = .1
    eqs_ears = '''
    dx/dt = (sound(t-delay)-x)/tau_ear+sigma_ear*(2./tau_ear)**.5*xi : 1 (unless refractory)
    delay = distance*sin(theta) : second
    distance : second # distance to the centre of the head in time units
    dtheta/dt = angular_speed : radian
    '''
    ears = NeuronGroup(2, eqs_ears, threshold='x>1', reset='x = 0',
                       refractory=2.5*ms, name='ears', method='euler')
    ears.distance = [-.5 * max_delay, .5 * max_delay]
    traces = StateMonitor(ears, 'delay', record=True)
    # Coincidence detectors
    num_neurons = 30
    tau = 1*ms
    sigma = .1
    eqs_neurons = '''
    dv/dt = -v / tau + sigma * (2 / tau)**.5 * xi : 1
    '''
    neurons = NeuronGroup(num_neurons, eqs_neurons, threshold='v>1',
                          reset='v = 0', name='neurons', method='euler')
    
    synapses = Synapses(ears, neurons, on_pre='v += .5')
    synapses.connect()
    
    synapses.delay['i==0'] = '(1.0*j)/(num_neurons-1)*1.1*max_delay'
    synapses.delay['i==1'] = '(1.0*(num_neurons-j-1))/(num_neurons-1)*1.1*max_delay'
    
    spikes = SpikeMonitor(neurons)
    
    run(1000*ms)
    
    # Plot the results
    i, t = spikes.it
    subplot(2, 1, 1)
    plot(t/ms, i, '.')
    xlabel('Time (ms)')
    ylabel('Neuron index')
    xlim(0, 1000)
    subplot(2, 1, 2)
    plot(traces.t/ms, traces.delay.T/ms)
    xlabel('Time (ms)')
    ylabel('Input delay (ms)')
    xlim(0, 1000)
    tight_layout()
    show()
    

![../_images/synapses.jeffress.1.png](../_images/synapses.jeffress.1.png)

---

# Example: lfp2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/compartmental.lfp.html

# Example: lfp

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/compartmental/lfp.ipynb)

Hodgkin-Huxley equations (1952)

We calculate the extracellular field potential at various places.
    
    
    from brian2 import *
    defaultclock.dt = 0.01*ms
    morpho = Cylinder(x=[0, 10]*cm, diameter=2*238*um, n=1000, type='axon')
    
    El = 10.613* mV
    ENa = 115*mV
    EK = -12*mV
    gl = 0.3*msiemens/cm**2
    gNa0 = 120*msiemens/cm**2
    gK = 36*msiemens/cm**2
    
    # Typical equations
    eqs = '''
    # The same equations for the whole neuron, but possibly different parameter values
    # distributed transmembrane current
    Im = gl * (El-v) + gNa * m**3 * h * (ENa-v) + gK * n**4 * (EK-v) : amp/meter**2
    I : amp (point current) # applied current
    dm/dt = alpham * (1-m) - betam * m : 1
    dn/dt = alphan * (1-n) - betan * n : 1
    dh/dt = alphah * (1-h) - betah * h : 1
    alpham = (0.1/mV) * 10*mV/exprel((-v+25*mV)/(10*mV))/ms : Hz
    betam = 4 * exp(-v/(18*mV))/ms : Hz
    alphah = 0.07 * exp(-v/(20*mV))/ms : Hz
    betah = 1/(exp((-v+30*mV) / (10*mV)) + 1)/ms : Hz
    alphan = (0.01/mV) * 10*mV/exprel((-v+10*mV)/(10*mV))/ms : Hz
    betan = 0.125*exp(-v/(80*mV))/ms : Hz
    gNa : siemens/meter**2
    '''
    
    neuron = SpatialNeuron(morphology=morpho, model=eqs, Cm=1*uF/cm**2,
                           Ri=35.4*ohm*cm, method="exponential_euler")
    neuron.v = 0*mV
    neuron.h = 1
    neuron.m = 0
    neuron.n = .5
    neuron.I = 0
    neuron.gNa = gNa0
    neuron[5*cm:10*cm].gNa = 0*siemens/cm**2
    M = StateMonitor(neuron, 'v', record=True)
    
    # LFP recorder
    Ne = 5 # Number of electrodes
    sigma = 0.3*siemens/meter # Resistivity of extracellular field (0.3-0.4 S/m)
    lfp = NeuronGroup(Ne, model='''v : volt
                                   x : meter
                                   y : meter
                                   z : meter''')
    lfp.x = 7*cm # Off center (to be far from stimulating electrode)
    lfp.y = [1*mm, 2*mm, 4*mm, 8*mm, 16*mm]
    S = Synapses(neuron, lfp, model='''w : ohm*meter**2 (constant) # Weight in the LFP calculation
                                       v_post = w*(Ic_pre-Im_pre) : volt (summed)''')
    S.summed_updaters['v_post'].when = 'after_groups'  # otherwise Ic has not yet been updated for the current time step.
    S.connect()
    S.w = 'area_pre/(4*pi*sigma)/((x_pre-x_post)**2+(y_pre-y_post)**2+(z_pre-z_post)**2)**.5'
    
    Mlfp = StateMonitor(lfp, 'v', record=True)
    
    run(50*ms, report='text')
    neuron.I[0] = 1*uA  # current injection at one end
    run(3*ms)
    neuron.I = 0*amp
    run(100*ms, report='text')
    
    subplot(211)
    for i in range(10):
        plot(M.t/ms, M.v[i*100]/mV)
    ylabel('$V_m$ (mV)')
    subplot(212)
    for i in range(5):
        plot(M.t/ms, Mlfp.v[i]/mV)
    ylabel('LFP (mV)')
    xlabel('Time (ms)')
    show()
    

![../_images/compartmental.lfp.1.png](../_images/compartmental.lfp.1.png)

---

# Example: licklider2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/synapses.licklider.html

# Example: licklider

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/synapses/licklider.ipynb)

Spike-based adaptation of Licklider’s model of pitch processing (autocorrelation with delay lines) with phase locking.
    
    
    from brian2 import *
    
    defaultclock.dt = .02 * ms
    
    # Ear and sound
    max_delay = 20*ms # 50 Hz
    tau_ear = 1*ms
    sigma_ear = 0.0
    eqs_ear = '''
    dx/dt = (sound-x)/tau_ear+0.1*(2./tau_ear)**.5*xi : 1 (unless refractory)
    sound = 5*sin(2*pi*frequency*t)**3 : 1 # nonlinear distortion
    #sound = 5*(sin(4*pi*frequency*t)+.5*sin(6*pi*frequency*t)) : 1 # missing fundamental
    frequency = (200+200*t*Hz)*Hz : Hz # increasing pitch
    '''
    receptors = NeuronGroup(2, eqs_ear, threshold='x>1', reset='x=0',
                            refractory=2*ms, method='euler')
    # Coincidence detectors
    min_freq = 50*Hz
    max_freq = 1000*Hz
    num_neurons = 300
    tau = 1*ms
    sigma = .1
    eqs_neurons = '''
    dv/dt = -v/tau+sigma*(2./tau)**.5*xi : 1
    '''
    
    neurons = NeuronGroup(num_neurons, eqs_neurons, threshold='v>1', reset='v=0',
                          method='euler')
    
    synapses = Synapses(receptors, neurons, on_pre='v += 0.5')
    synapses.connect()
    synapses.delay = 'i*1.0/exp(log(min_freq/Hz)+(j*1.0/(num_neurons-1))*log(max_freq/min_freq))*second'
    
    spikes = SpikeMonitor(neurons)
    
    run(500*ms)
    plot(spikes.t/ms, spikes.i, '.k')
    xlabel('Time (ms)')
    ylabel('Frequency')
    yticks([0, 99, 199, 299],
           array(1. / synapses.delay[1, [0, 99, 199, 299]], dtype=int))
    show()
    

![../_images/synapses.licklider.1.png](../_images/synapses.licklider.1.png)

---

# Example: modelfitting_sbi2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/advanced.modelfitting_sbi.html

# Example: modelfitting_sbi

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/advanced/modelfitting_sbi.ipynb)

## Model fitting with simulation-based inference

In this example, a HH-type model is used to demonstrate simulation-based inference with the sbi toolbox (<https://www.mackelab.org/sbi/>). It is based on a fake current-clamp recording generated from the same model that we use in the inference process. Two of the parameters (the maximum sodium and potassium conductances) are considered parameters of the model.

For more details about this approach, see the references below.

To run this example, you need to install the sbi package, e.g. with:
    
    
    pip install sbi
    

References:

  * <https://www.mackelab.org/sbi>

  * Tejero-Cantero et al., (2020). sbi: A toolkit for simulation-based inference. Journal of Open Source Software, 5(52), 2505, <https://doi.org/10.21105/joss.02505>

    
    
    import matplotlib.pyplot as plt
    
    from brian2 import *
    import sbi.utils
    import sbi.analysis
    import sbi.inference
    import torch  # PyTorch
    
    defaultclock.dt = 0.05*ms
    
    def simulate(params, I=1*nA, t_on=50*ms, t_total=350*ms):
        """
        Simulates the HH-model with Brian2 for parameter sets in params and the
        given input current (injection of I between t_on and t_total-t_on).
    
        Returns a dictionary {'t': time steps, 'v': voltage,
                              'I_inj': current, 'spike_count': spike count}.
        """
        assert t_total > 2*t_on
        t_off = t_total - t_on
    
        params = np.atleast_2d(params)
        # fixed parameters
        gleak = 10*nS
        Eleak = -70*mV
        VT = -60.0*mV
        C = 200*pF
        ENa = 53*mV
        EK = -107*mV
    
        # The conductance-based model
        eqs = '''
             dVm/dt = -(gNa*m**3*h*(Vm - ENa) + gK*n**4*(Vm - EK) + gleak*(Vm - Eleak) - I_inj) / C : volt
             I_inj = int(t >= t_on and t < t_off)*I : amp (shared)
             dm/dt = alpham*(1-m) - betam*m : 1
             dn/dt = alphan*(1-n) - betan*n : 1
             dh/dt = alphah*(1-h) - betah*h : 1
    
             alpham = (-0.32/mV) * (Vm - VT - 13.*mV) / (exp((-(Vm - VT - 13.*mV))/(4.*mV)) - 1)/ms : Hz
             betam = (0.28/mV) * (Vm - VT - 40.*mV) / (exp((Vm - VT - 40.*mV)/(5.*mV)) - 1)/ms : Hz
    
             alphah = 0.128 * exp(-(Vm - VT - 17.*mV) / (18.*mV))/ms : Hz
             betah = 4/(1 + exp((-(Vm - VT - 40.*mV)) / (5.*mV)))/ms : Hz
    
             alphan = (-0.032/mV) * (Vm - VT - 15.*mV) / (exp((-(Vm - VT - 15.*mV)) / (5.*mV)) - 1)/ms : Hz
             betan = 0.5*exp(-(Vm - VT - 10.*mV) / (40.*mV))/ms : Hz
             # The parameters to fit
             gNa : siemens (constant)
             gK : siemens (constant)
             '''
        neurons = NeuronGroup(params.shape[0], eqs, threshold='m>0.5', refractory='m>0.5',
                              method='exponential_euler', name='neurons')
        Vm_mon = StateMonitor(neurons, 'Vm', record=True, name='Vm_mon')
        spike_mon = SpikeMonitor(neurons, record=False, name='spike_mon')  #record=False → do not record times
        neurons.gNa_ = params[:, 0]*uS
        neurons.gK = params[:, 1]*uS
    
        neurons.Vm = 'Eleak'
        neurons.m = '1/(1 + betam/alpham)'         # Would be the solution when dm/dt = 0
        neurons.h = '1/(1 + betah/alphah)'         # Would be the solution when dh/dt = 0
        neurons.n = '1/(1 + betan/alphan)'         # Would be the solution when dn/dt = 0
    
        run(t_total)
        # For convenient plotting, reconstruct the current
        I_inj = ((Vm_mon.t >= t_on) & (Vm_mon.t < t_off))*I
        return dict(v=Vm_mon.Vm,
                    t=Vm_mon.t,
                    I_inj=I_inj,
                    spike_count=spike_mon.count)
    
    
    def calculate_summary_statistics(x):
        """Calculate summary statistics for results in x"""
        I_inj = x["I_inj"]
        v = x["v"]/mV
    
        spike_count = x["spike_count"]
        # Mean and standard deviation during stimulation
        v_active = v[:, I_inj > 0*nA]
        mean_active = np.mean(v_active, axis=1)
        std_active = np.std(v_active, axis=1)
        # Height of action potential peaks
        max_v = np.max(v_active, axis=1)
    
        # concatenation of summary statistics
        sum_stats = np.vstack((spike_count, mean_active, std_active, max_v))
    
        return sum_stats.T
    
    
    def simulation_wrapper(params):
        """
        Returns summary statistics from conductance values in `params`.
        Summarizes the output of the simulation and converts it to `torch.Tensor`.
        """
        obs = simulate(params)
        summstats = torch.as_tensor(calculate_summary_statistics(obs))
        return summstats.to(torch.float32)
    
    
    if __name__ == '__main__':
        # Define prior distribution over parameters
        prior_min = [.5, 1e-4]  # (gNa, gK) in µS
        prior_max = [80.,15.]
        prior = sbi.utils.torchutils.BoxUniform(low=torch.as_tensor(prior_min),
                                                high=torch.as_tensor(prior_max))
    
        # Simulate samples from the prior distribution
        theta = prior.sample((10_000,))
        print('Simulating samples from prior simulation... ', end='')
        stats = simulation_wrapper(theta.numpy())
        print('done.')
    
        # Train inference network
        density_estimator_build_fun = sbi.utils.posterior_nn(model='mdn')
        inference = sbi.inference.SNPE(prior,
                                       density_estimator=density_estimator_build_fun)
        print('Training inference network... ')
        inference.append_simulations(theta, stats).train()
        posterior = inference.build_posterior()
    
        # true parameters for real ground truth data
        true_params = np.array([[32., 1.]])
        true_data = simulate(true_params)
        t = true_data['t']
        I_inj = true_data['I_inj']
        v = true_data['v']
        xo = calculate_summary_statistics(true_data)
        print("The true summary statistics are:  ", xo)
    
        # Plot estimated posterior distribution
        samples = posterior.sample((1000,), x=xo, show_progress_bars=False)
        labels_params = [r'$\overline{g}_{Na}$', r'$\overline{g}_{K}$']
        sbi.analysis.pairplot(samples,
                              limits=[[.5, 80], [1e-4, 15.]],
                              ticks=[[.5, 80], [1e-4, 15.]],
                              figsize=(4, 4),
                              points=true_params, labels=labels_params,
                              points_offdiag={'markersize': 6},
                              points_colors=['r'])
        plt.tight_layout()
    
        # Draw a single sample from the posterior and convert to numpy for plotting.
        posterior_sample = posterior.sample((1,), x=xo,
                                            show_progress_bars=False).numpy()
        x = simulate(posterior_sample)
    
        # plot observation and sample
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(t/ms, v[0, :]/mV, lw=2, label='observation')
        ax.plot(t/ms, x['v'][0, :]/mV, '--', lw=2, label='posterior sample')
        ax.legend()
        ax.set(xlabel='time (ms)', ylabel='voltage (mV)')
        plt.show()
    

![../_images/advanced.modelfitting_sbi.1.png](../_images/advanced.modelfitting_sbi.1.png) ![../_images/advanced.modelfitting_sbi.2.png](../_images/advanced.modelfitting_sbi.2.png)

---

# Example: morphotest2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/compartmental.morphotest.html

# Example: morphotest

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/compartmental/morphotest.ipynb)

Demonstrate the usage of the [`Morphology`](../reference/brian2.spatialneuron.morphology.Morphology.html#brian2.spatialneuron.morphology.Morphology "brian2.spatialneuron.morphology.Morphology") object.
    
    
    from brian2 import *
    
    # Morphology
    morpho = Soma(30*um)
    morpho.L = Cylinder(diameter=1*um, length=100*um, n=5)
    morpho.LL = Cylinder(diameter=1*um, length=20*um, n=2)
    morpho.R = Cylinder(diameter=1*um, length=100*um, n=5)
    
    # Passive channels
    gL = 1e-4*siemens/cm**2
    EL = -70*mV
    eqs = '''
    Im = gL * (EL-v) : amp/meter**2
    '''
    
    neuron = SpatialNeuron(morphology=morpho, model=eqs,
                           Cm=1*uF/cm**2, Ri=100*ohm*cm, method='exponential_euler')
    neuron.v = arange(0, 13)*volt
    
    print(neuron.v)
    print(neuron.L.v)
    print(neuron.LL.v)
    print(neuron.L.main.v)
    

---

# Example: non_reliability2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/non_reliability.html

# Example: non_reliability

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/non_reliability.ipynb)

Reliability of spike timing.

See e.g. Mainen & Sejnowski (1995) for experimental results in vitro.

Here: a constant current is injected in all trials.
    
    
    from brian2 import *
    
    N = 25
    tau = 20*ms
    sigma = .015
    eqs_neurons = '''
    dx/dt = (1.1 - x) / tau + sigma * (2 / tau)**.5 * xi : 1 (unless refractory)
    '''
    neurons = NeuronGroup(N, model=eqs_neurons, threshold='x > 1', reset='x = 0',
                          refractory=5*ms, method='euler')
    spikes = SpikeMonitor(neurons)
    
    run(500*ms)
    plot(spikes.t/ms, spikes.i, '.k')
    xlabel('Time (ms)')
    ylabel('Neuron index')
    show()
    

![../_images/non_reliability.1.png](../_images/non_reliability.1.png)

---

# Example: nonlinear2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/synapses.nonlinear.html

# Example: nonlinear

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/synapses/nonlinear.ipynb)

NMDA synapses.
    
    
    from brian2 import *
    
    a = 1 / (10*ms)
    b = 1 / (10*ms)
    c = 1 / (10*ms)
    
    neuron_input = NeuronGroup(2, 'dv/dt = 1/(10*ms) : 1', threshold='v>1', reset='v = 0',
                        method='euler')
    neurons = NeuronGroup(1, """dv/dt = (g-v)/(10*ms) : 1
                                g : 1""", method='exact')
    S = Synapses(neuron_input, neurons, '''
                    dg_syn/dt = -a*g_syn+b*x*(1-g_syn) : 1 (clock-driven)
                    g_post = g_syn : 1 (summed)
                    dx/dt=-c*x : 1 (clock-driven)
                    w : 1 # synaptic weight
                 ''', on_pre='x += w') # NMDA synapses
    
    S.connect()
    S.w = [1., 10.]
    neuron_input.v = [0., 0.5]
    
    M = StateMonitor(S, 'g',
                     # If not using standalone mode, this could also simply be
                     # record=True
                     record=np.arange(len(neuron_input)*len(neurons)))
    Mn = StateMonitor(neurons, 'g', record=0)
    
    run(1000*ms)
    
    subplot(2, 1, 1)
    plot(M.t/ms, M.g.T)
    xlabel('Time (ms)')
    ylabel('g_syn')
    subplot(2, 1, 2)
    plot(Mn.t/ms, Mn[0].g)
    ylabel('Time (ms)')
    ylabel('g')
    tight_layout()
    show()
    

![../_images/synapses.nonlinear.1.png](../_images/synapses.nonlinear.1.png)

---

# Example: opencv_movie2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/advanced.opencv_movie.html

# Example: opencv_movie

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/advanced/opencv_movie.ipynb)

An example that uses a function from external C library (OpenCV in this case). Works for all C-based code generation targets (i.e. for cython and cpp_standalone device) and for numpy (using the Python bindings).

This example needs a working installation of OpenCV 3.x and its Python bindings. It has been tested on 64 bit Linux in a conda environment with packages from the `conda-forge` channels (opencv 3.4.4, x264 1!152.20180717, ffmpeg 4.1).
    
    
    import os
    import urllib.request, urllib.error, urllib.parse
    import cv2  # Import OpenCV2
    
    from brian2 import *
    
    defaultclock.dt = 1*ms
    prefs.codegen.target = 'cython'
    prefs.logging.std_redirection = False
    set_device('cpp_standalone', clean=True)
    filename = os.path.abspath('Megamind.avi')
    
    if not os.path.exists(filename):
        print('Downloading the example video file')
        response = urllib.request.urlopen('http://docs.opencv.org/2.4/_downloads/Megamind.avi')
        data = response.read()
        with open(filename, 'wb') as f:
            f.write(data)
    
    video = cv2.VideoCapture(filename)
    width, height, frame_count = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                  int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                                  int(video.get(cv2.CAP_PROP_FRAME_COUNT)))
    fps = 24
    time_between_frames = 1*second/fps
    
    @implementation('cpp', '''
    double* get_frame(bool new_frame)
    {
        // The following initializations will only be executed once
        static cv::VideoCapture source("VIDEO_FILENAME");
        static cv::Mat frame;
        static double* grayscale_frame = (double*)malloc(VIDEO_WIDTH*VIDEO_HEIGHT*sizeof(double));
        if (new_frame)
        {
            source >> frame;
            double mean_value = 0;
            for (int row=0; row<VIDEO_HEIGHT; row++)
                for (int col=0; col<VIDEO_WIDTH; col++)
                {
                    const double grayscale_value = (frame.at<cv::Vec3b>(row, col)[0] +
                                                    frame.at<cv::Vec3b>(row, col)[1] +
                                                    frame.at<cv::Vec3b>(row, col)[2])/(3.0*128);
                    mean_value += grayscale_value / (VIDEO_WIDTH * VIDEO_HEIGHT);
                    grayscale_frame[row*VIDEO_WIDTH + col] = grayscale_value;
                }
            // subtract the mean
            for (int i=0; i<VIDEO_HEIGHT*VIDEO_WIDTH; i++)
                grayscale_frame[i] -= mean_value;
        }
        return grayscale_frame;
    }
    
    double video_input(const int x, const int y)
    {
        // Get the current frame (or a new frame in case we are asked for the first
        // element
        double *frame = get_frame(x==0 && y==0);
        return frame[y*VIDEO_WIDTH + x];
    }
    '''.replace('VIDEO_FILENAME', filename),
                    libraries=['opencv_core',
                               'opencv_highgui',
                               'opencv_videoio'],
                    headers=['<opencv2/core/core.hpp>',
                             '<opencv2/highgui/highgui.hpp>'],
                    define_macros=[('VIDEO_WIDTH', width),
                                   ('VIDEO_HEIGHT', height)])
    @check_units(x=1, y=1, result=1)
    def video_input(x, y):
        # we assume this will only be called in the custom operation (and not for
        # example in a reset or synaptic statement), so we don't need to do indexing
        # but we can directly return the full result
        _, frame = video.read()
        grayscale = frame.mean(axis=2)
        grayscale /= 128.  # scale everything between 0 and 2
        return grayscale.ravel() - grayscale.ravel().mean()
    
    
    N = width * height
    tau, tau_th = 10*ms, time_between_frames
    G = NeuronGroup(N, '''dv/dt = (-v + I)/tau : 1
                          dv_th/dt = -v_th/tau_th : 1
                          row : integer (constant)
                          column : integer (constant)
                          I : 1 # input current''',
                    threshold='v>v_th', reset='v=0; v_th = 3*v_th + 1.0',
                    method='exact')
    G.v_th = 1
    G.row = 'i//width'
    G.column = 'i%width'
    
    G.run_regularly('I = video_input(column, row)',
                    dt=time_between_frames)
    mon = SpikeMonitor(G)
    runtime = frame_count*time_between_frames
    run(runtime, report='text')
    
    # Avoid going through the whole Brian2 indexing machinery too much
    i, t, row, column = mon.i[:], mon.t[:], G.row[:], G.column[:]
    
    import matplotlib.animation as animation
    
    # TODO: Use overlapping windows
    stepsize = 100*ms
    def next_spikes():
        step = next_spikes.step
        if step*stepsize > runtime:
            next_spikes.step=0
            raise StopIteration()
        spikes = i[(t>=step*stepsize) & (t<(step+1)*stepsize)]
        next_spikes.step += 1
        yield column[spikes], row[spikes]
    next_spikes.step = 0
    
    fig, ax = plt.subplots()
    dots, = ax.plot([], [], 'k.', markersize=2, alpha=.25)
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.invert_yaxis()
    def run(data):
        x, y = data
        dots.set_data(x, y)
    
    ani = animation.FuncAnimation(fig, run, next_spikes, blit=False, repeat=True,
                                  repeat_delay=1000)
    plt.show()
    

---

# Example: phase_locking2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/phase_locking.html

# Example: phase_locking

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/phase_locking.ipynb)

Phase locking of IF neurons to a periodic input.
    
    
    from brian2 import *
    
    tau = 20*ms
    n = 100
    b = 1.2 # constant current mean, the modulation varies
    freq = 10*Hz
    
    eqs = '''
    dv/dt = (-v + a * sin(2 * pi * freq * t) + b) / tau : 1
    a : 1
    '''
    neurons = NeuronGroup(n, model=eqs, threshold='v > 1', reset='v = 0',
                          method='euler')
    neurons.v = 'rand()'
    neurons.a = '0.05 + 0.7*i/n'
    S = SpikeMonitor(neurons)
    trace = StateMonitor(neurons, 'v', record=50)
    
    run(1000*ms)
    subplot(211)
    plot(S.t/ms, S.i, '.k')
    xlabel('Time (ms)')
    ylabel('Neuron index')
    subplot(212)
    plot(trace.t/ms, trace.v.T)
    xlabel('Time (ms)')
    ylabel('v')
    tight_layout()
    show()
    

![../_images/phase_locking.1.png](../_images/phase_locking.1.png)

---

# Example: rall2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/compartmental.rall.html

# Example: rall

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/compartmental/rall.ipynb)

A cylinder plus two branches, with diameters according to Rall’s formula
    
    
    from brian2 import *
    
    defaultclock.dt = 0.01*ms
    
    # Passive channels
    gL = 1e-4*siemens/cm**2
    EL = -70*mV
    
    # Morphology
    diameter = 1*um
    length = 300*um
    Cm = 1*uF/cm**2
    Ri = 150*ohm*cm
    N = 500
    rm = 1 / (gL * pi * diameter)  # membrane resistance per unit length
    ra = (4 * Ri)/(pi * diameter**2)  # axial resistance per unit length
    la = sqrt(rm / ra) # space length
    morpho = Cylinder(diameter=diameter, length=length, n=N)
    d1 = 0.5*um
    L1 = 200*um
    rm = 1 / (gL * pi * d1) # membrane resistance per unit length
    ra = (4 * Ri) / (pi * d1**2) # axial resistance per unit length
    l1 = sqrt(rm / ra) # space length
    morpho.L = Cylinder(diameter=d1, length=L1, n=N)
    d2 = (diameter**1.5 - d1**1.5)**(1. / 1.5)
    rm = 1/(gL * pi * d2) # membrane resistance per unit length
    ra = (4 * Ri) / (pi * d2**2) # axial resistance per unit length
    l2 = sqrt(rm / ra) # space length
    L2 = (L1 / l1) * l2
    morpho.R = Cylinder(diameter=d2, length=L2, n=N)
    
    eqs='''
    Im = gL * (EL-v) : amp/meter**2
    I : amp (point current)
    '''
    
    neuron = SpatialNeuron(morphology=morpho, model=eqs, Cm=Cm, Ri=Ri,
                           method='exponential_euler')
    neuron.v = EL
    
    neuron.I[0] = 0.02*nA # injecting at the left end
    run(100*ms, report='text')
    
    plot(neuron.main.distance/um, neuron.main.v/mV, 'k')
    plot(neuron.L.distance/um, neuron.L.v/mV, 'k')
    plot(neuron.R.distance/um, neuron.R.v/mV, 'k')
    # Theory
    x = neuron.main.distance
    ra = la * 4 * Ri/(pi * diameter**2)
    l = length/la + L1/l1
    theory = EL + ra*neuron.I[0]*cosh(l - x/la)/sinh(l)
    plot(x/um, theory/mV, 'r')
    x = neuron.L.distance
    theory = (EL+ra*neuron.I[0]*cosh(l - neuron.main.distance[-1]/la -
                                     (x - neuron.main.distance[-1])/l1)/sinh(l))
    plot(x/um, theory/mV, 'r')
    x = neuron.R.distance
    theory = (EL+ra*neuron.I[0]*cosh(l - neuron.main.distance[-1]/la -
                                     (x - neuron.main.distance[-1])/l2)/sinh(l))
    plot(x/um, theory/mV, 'r')
    xlabel('x (um)')
    ylabel('v (mV)')
    show()
    

![../_images/compartmental.rall.1.png](../_images/compartmental.rall.1.png)

---

# Example: reliability2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/reliability.html

# Example: reliability

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/reliability.ipynb)

Reliability of spike timing.

See e.g. Mainen & Sejnowski (1995) for experimental results in vitro.
    
    
    from brian2 import *
    
    # The common noisy input
    N = 25
    tau_input = 5*ms
    neuron_input = NeuronGroup(1, 'dx/dt = -x / tau_input + (2 /tau_input)**.5 * xi : 1')
    
    # The noisy neurons receiving the same input
    tau = 10*ms
    sigma = .015
    eqs_neurons = '''
    dx/dt = (0.9 + .5 * I - x) / tau + sigma * (2 / tau)**.5 * xi : 1
    I : 1 (linked)
    '''
    neurons = NeuronGroup(N, model=eqs_neurons, threshold='x > 1',
                          reset='x = 0', refractory=5*ms, method='euler')
    neurons.x = 'rand()'
    neurons.I = linked_var(neuron_input, 'x') # input.x is continuously fed into neurons.I
    spikes = SpikeMonitor(neurons)
    
    run(500*ms)
    plt.plot(spikes.t/ms, spikes.i, '.k')
    xlabel('Time (ms)')
    ylabel('Neuron index')
    show()
    

![../_images/reliability.1.png](../_images/reliability.1.png)

---

# Example: simple_case2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/standalone.simple_case.html

# Example: simple_case

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/standalone/simple_case.ipynb)

The most simple case how to use standalone mode.
    
    
    from brian2 import *
    set_device('cpp_standalone')  # ← only difference to "normal" simulation
    
    tau = 10*ms
    eqs = '''
    dv/dt = (1-v)/tau : 1
    '''
    G = NeuronGroup(10, eqs, method='exact')
    G.v = 'rand()'
    mon = StateMonitor(G, 'v', record=True)
    run(100*ms)
    
    plt.plot(mon.t/ms, mon.v.T)
    plt.gca().set(xlabel='t (ms)', ylabel='v')
    plt.show()
    

![../_images/standalone.simple_case.1.png](../_images/standalone.simple_case.1.png)

---

# Example: simple_case_build2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/standalone.simple_case_build.html

# Example: simple_case_build

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/standalone/simple_case_build.ipynb)

The most simple case how to use standalone mode with several [`run()`](../reference/brian2.core.magic.run.html#brian2.core.magic.run "brian2.core.magic.run") calls.
    
    
    from brian2 import *
    set_device('cpp_standalone', build_on_run=False)
    
    tau = 10*ms
    I = 1  # input current
    eqs = '''
    dv/dt = (I-v)/tau : 1
    '''
    G = NeuronGroup(10, eqs, method='exact')
    G.v = 'rand()'
    mon = StateMonitor(G, 'v', record=True)
    run(20*ms)
    I = 0
    run(80*ms)
    # Actually generate/compile/run the code:
    device.build()
    
    plt.plot(mon.t/ms, mon.v.T)
    plt.gca().set(xlabel='t (ms)', ylabel='v')
    plt.show()
    

![../_images/standalone.simple_case_build.1.png](../_images/standalone.simple_case_build.1.png)

---

# Example: spatial_connections2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/synapses.spatial_connections.html

# Example: spatial_connections

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/synapses/spatial_connections.ipynb)

A simple example showing how string expressions can be used to implement spatial (deterministic or stochastic) connection patterns.
    
    
    from brian2 import *
    
    rows, cols = 20, 20
    G = NeuronGroup(rows * cols, '''x : meter
                                    y : meter''')
    # initialize the grid positions
    grid_dist = 25*umeter
    G.x = '(i // rows) * grid_dist - rows/2.0 * grid_dist'
    G.y = '(i % rows) * grid_dist - cols/2.0 * grid_dist'
    
    # Deterministic connections
    distance = 120*umeter
    S_deterministic = Synapses(G, G)
    S_deterministic.connect('sqrt((x_pre - x_post)**2 + (y_pre - y_post)**2) < distance')
    
    # Random connections (no self-connections)
    S_stochastic = Synapses(G, G)
    S_stochastic.connect('i != j',
                         p='1.5 * exp(-((x_pre-x_post)**2 + (y_pre-y_post)**2)/(2*(60*umeter)**2))')
    
    figure(figsize=(12, 6))
    
    # Show the connections for some neurons in different colors
    for color in ['g', 'b', 'm']:
        subplot(1, 2, 1)
        neuron_idx = np.random.randint(0, rows*cols)
        plot(G.x[neuron_idx] / umeter, G.y[neuron_idx] / umeter, 'o', mec=color,
             mfc='none')
        plot(G.x[S_deterministic.j[neuron_idx, :]] / umeter,
             G.y[S_deterministic.j[neuron_idx, :]] / umeter, color + '.')
        subplot(1, 2, 2)
        plot(G.x[neuron_idx] / umeter, G.y[neuron_idx] / umeter, 'o', mec=color,
             mfc='none')
        plot(G.x[S_stochastic.j[neuron_idx, :]] / umeter,
             G.y[S_stochastic.j[neuron_idx, :]] / umeter, color + '.')
    
    for idx, t in enumerate(['determininstic connections',
                             'random connections']):
        subplot(1, 2, idx + 1)
        xlim((-rows/2.0 * grid_dist) / umeter, (rows/2.0 * grid_dist) / umeter)
        ylim((-cols/2.0 * grid_dist) / umeter, (cols/2.0 * grid_dist) / umeter)
        title(t)
        xlabel('x')
        ylabel('y', rotation='horizontal')
        axis('equal')
    
    tight_layout()
    show()
    

![../_images/synapses.spatial_connections.1.png](../_images/synapses.spatial_connections.1.png)

---

# Example: spike_based_homeostasis2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/synapses.spike_based_homeostasis.html

# Example: spike_based_homeostasis

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/synapses/spike_based_homeostasis.ipynb)

Following O. Breitwieser: “Towards a Neuromorphic Implementation of Spike-Based Expectation Maximization”

Two poisson stimuli are connected to a neuron. One with a varying rate and the other with a fixed rate. The synaptic weight from the varying rate stimulus to the neuron is fixed. The synaptic weight from the fixed rate stimulus to the neuron is plastic and tries to keep the neuron at a firing rate that is determined by the parameters of the plasticity rule.

Sebastian Schmitt, 2021
    
    
    import itertools
    import numpy as np
    import matplotlib.pyplot as plt
    
    from brian2 import TimedArray, PoissonGroup, NeuronGroup, Synapses, StateMonitor, PopulationRateMonitor
    from brian2 import defaultclock, run
    from brian2 import Hz, ms, second
    
    # The synaptic weight from the steady stimulus is plastic
    steady_stimulus = TimedArray([50]*Hz, dt=40*second)
    steady_poisson = PoissonGroup(1, rates='steady_stimulus(t)')
    
    # The synaptic weight from the varying stimulus is static
    varying_stimulus = TimedArray([25*Hz, 50*Hz, 0*Hz, 35*Hz, 0*Hz], dt=10*second)
    varying_poisson = PoissonGroup(1, rates='varying_stimulus(t)')
    
    # dw_plus/dw_minus determines scales the steady stimulus rate to the target firing rate, must not be larger 1
    # the magntude of dw_plus and dw_minus determines the "speed" of the homeostasis
    parameters = {
        'tau': 10*ms,  # membrane time constant
        'dw_plus': 0.05,  # weight increment on pre spike
        'dw_minus': 0.05,  # weight increment on post spike
        'w_max': 2,  # maximum plastic weight
        'w_initial': 0  # initial plastic weight
    }
    
    eqs = 'dv/dt = (0 - v)/tau : 1 (unless refractory)'
    
    neuron_with_homeostasis = NeuronGroup(1, eqs,
                                          threshold='v > 1', reset='v = -1',
                                          method='euler', refractory=1*ms,
                                          namespace=parameters)
    neuron_without_homeostasis = NeuronGroup(1, eqs,
                                             threshold='v > 1', reset='v = -1',
                                             method='euler', refractory=1*ms,
                                             namespace=parameters)
    
    plastic_synapse = Synapses(steady_poisson, neuron_with_homeostasis,
                               'w : 1',
                               on_pre='''
                               v_post += w
                               w = clip(w + dw_plus, 0, w_max)
                               ''',
                               on_post='''
                               w = clip(w - dw_minus, 0, w_max)
                               ''', namespace=parameters)
    plastic_synapse.connect()
    plastic_synapse.w = parameters['w_initial']
    
    non_plastic_synapse_neuron_without_homeostasis = Synapses(varying_poisson,
                                                              neuron_without_homeostasis,
                                                              'w : 1', on_pre='v_post += w')
    non_plastic_synapse_neuron_without_homeostasis.connect()
    non_plastic_synapse_neuron_without_homeostasis.w = 2
    
    non_plastic_synapse_neuron = Synapses(varying_poisson, neuron_with_homeostasis,
                                          'w : 1', on_pre='v_post += w')
    non_plastic_synapse_neuron.connect()
    non_plastic_synapse_neuron.w = 2
    
    M = StateMonitor(neuron_with_homeostasis, 'v', record=True)
    M2 = StateMonitor(plastic_synapse, 'w', record=True)
    M_rate_neuron_with_homeostasis = PopulationRateMonitor(neuron_with_homeostasis)
    M_rate_neuron_without_homeostasis = PopulationRateMonitor(neuron_without_homeostasis)
    
    duration = 40*second
    defaultclock.dt = 0.1*ms
    run(duration, report='text')
    
    fig, axes = plt.subplots(3, sharex=True)
    
    axes[0].plot(M2.t/second, M2.w[0], label="homeostatic weight")
    axes[0].set_ylabel("weight")
    axes[0].legend()
    
    # dt is in second
    dts = np.arange(0., len(varying_stimulus.values)*varying_stimulus.dt, varying_stimulus.dt)
    x = list(itertools.chain(*zip(dts, dts)))
    y = list(itertools.chain(*zip(varying_stimulus.values/Hz, varying_stimulus.values/Hz)))
    axes[1].plot(x, [0] + y[:-1], label="varying stimulus")
    axes[1].set_ylabel("rate [Hz]")
    axes[1].legend()
    
    # in ms
    smooth_width = 100*ms
    axes[2].plot(M_rate_neuron_with_homeostasis.t/second,
                 M_rate_neuron_with_homeostasis.smooth_rate(width=smooth_width)/Hz,
                 label="with homeostasis")
    axes[2].plot(M_rate_neuron_without_homeostasis.t/second,
                 M_rate_neuron_without_homeostasis.smooth_rate(width=smooth_width)/Hz,
                 label="without homeostasis")
    axes[2].set_ylabel("firing rate [Hz]")
    axes[2].legend()
    
    plt.xlabel('Time (s)')
    plt.show()
    

![../_images/synapses.spike_based_homeostasis.1.png](../_images/synapses.spike_based_homeostasis.1.png)

---

# Example: spike_initiation2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/compartmental.spike_initiation.html

# Example: spike_initiation

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/compartmental/spike_initiation.ipynb)

Ball and stick with Na and K channels
    
    
    from brian2 import *
    
    defaultclock.dt = 0.025*ms
    
    # Morphology
    morpho = Soma(30*um)
    morpho.axon = Cylinder(diameter=1*um, length=300*um, n=100)
    
    # Channels
    gL = 1e-4*siemens/cm**2
    EL = -70*mV
    ENa = 50*mV
    ka = 6*mV
    ki = 6*mV
    va = -30*mV
    vi = -50*mV
    EK = -90*mV
    vk = -20*mV
    kk = 8*mV
    eqs = '''
    Im = gL*(EL-v)+gNa*m*h*(ENa-v)+gK*n*(EK-v) : amp/meter**2
    dm/dt = (minf-m)/(0.3*ms) : 1 # simplified Na channel
    dh/dt = (hinf-h)/(3*ms) : 1 # inactivation
    dn/dt = (ninf-n)/(5*ms) : 1 # K+
    minf = 1/(1+exp((va-v)/ka)) : 1
    hinf = 1/(1+exp((v-vi)/ki)) : 1
    ninf = 1/(1+exp((vk-v)/kk)) : 1
    I : amp (point current)
    gNa : siemens/meter**2
    gK : siemens/meter**2
    '''
    
    neuron = SpatialNeuron(morphology=morpho, model=eqs,
                           Cm=1*uF/cm**2, Ri=100*ohm*cm, method='exponential_euler')
    neuron.v = -65*mV
    neuron.I = 0*amp
    neuron.axon[30*um:60*um].gNa = 700*gL
    neuron.axon[30*um:60*um].gK = 700*gL
    
    # Monitors
    mon=StateMonitor(neuron, 'v', record=True)
    
    run(1*ms)
    neuron.main.I = 0.15*nA
    run(50*ms)
    neuron.I = 0*amp
    run(95*ms, report='text')
    
    plot(mon.t/ms, mon.v[0]/mV, 'r')
    plot(mon.t/ms, mon.v[20]/mV, 'g')
    plot(mon.t/ms, mon.v[40]/mV, 'b')
    plot(mon.t/ms, mon.v[60]/mV, 'k')
    plot(mon.t/ms, mon.v[80]/mV, 'y')
    xlabel('Time (ms)')
    ylabel('v (mV)')
    show()
    

![../_images/compartmental.spike_initiation.1.png](../_images/compartmental.spike_initiation.1.png)

---

# Example: standalone_multiple_processes2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/standalone.standalone_multiple_processes.html

# Example: standalone_multiple_processes

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/standalone/standalone_multiple_processes.ipynb)

This example shows how to run several, independent simulations in standalone mode using multiple processes to run the simulations in parallel. Given that this example only involves a single neuron, an alternative – and arguably more elegant – solution would be to run the simulations in a single [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup"), where each neuron receives input with a different rate.

The example is a standalone equivalent of the one presented in /tutorials/3-intro-to-brian-simulations.

Note that Python’s [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing "\(in Python v3.12\)") module cannot deal with user-defined functions (including [`TimedArray`](../reference/brian2.input.timedarray.TimedArray.html#brian2.input.timedarray.TimedArray "brian2.input.timedarray.TimedArray")) and other complex code structures. If you run into `PicklingError` or [`AttributeError`](https://docs.python.org/3/library/exceptions.html#AttributeError "\(in Python v3.12\)") exceptions, you might have to use the `pathos` (<https://pypi.org/project/pathos>) package instead, which can handle more complex code structures.
    
    
    import numpy as np
    import matplotlib.pyplot as plt
    import brian2 as b2
    from time import time
    
    b2.set_device('cpp_standalone', build_on_run=False)
    
    class SimWrapper:
        def __init__(self):
            self.net = b2.Network()
            P = b2.PoissonGroup(num_inputs, rates=input_rate)
            eqs = """
                dv/dt = -v/tau : 1
                tau : second (constant)
                """
            G = b2.NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='euler', name='neuron')
            S = b2.Synapses(P, G, on_pre='v += weight')
            S.connect()
            M = b2.SpikeMonitor(G, name='spike_monitor')
            self.net.add([P, G, S, M])
    
            self.net.run(1000 * b2.ms)
    
            self.device = b2.get_device()
            self.device.build(run=False, directory=None)  # compile the code, but don't run it yet
    
        def do_run(self, tau_i):
            # Workaround to set the device globally in this context
            from brian2.devices import device_module
            device_module.active_device = self.device
    
            result_dir = f'result_{tau_i}'
            self.device.run(run_args={self.net['neuron'].tau: tau_i},
                            results_directory=result_dir)
            return self.net["spike_monitor"].num_spikes/ b2.second
    
    
    if __name__ == "__main__":
        start_time = time()
        num_inputs = 100
        input_rate = 10 * b2.Hz
        weight = 0.1
    
        npoints = 15
        tau_range = np.linspace(1, 15, npoints) * b2.ms
    
        sim = SimWrapper()
    
        from multiprocessing import Pool
        with Pool(npoints) as pool:
            output_rates = pool.map(sim.do_run, tau_range)
    
        print(f"Done in {time() - start_time}")
    
        plt.plot(tau_range/b2.ms, output_rates)
        plt.xlabel(r"$\tau$ (ms)")
        plt.ylabel("Firing rate (sp/s)")
        plt.show()
    

![../_images/standalone.standalone_multiple_processes.1.png](../_images/standalone.standalone_multiple_processes.1.png)

---

# Example: standalone_multiplerun2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/standalone.standalone_multiplerun.html

# Example: standalone_multiplerun

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/standalone/standalone_multiplerun.ipynb)

This example shows how to run several, independent simulations in standalone mode. Given that this example only involves a single neuron, an alternative – and arguably more elegant – solution would be to run the simulations in a single [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup"), where each neuron receives input with a different rate.

The example is a standalone equivalent of the one presented in /tutorials/3-intro-to-brian-simulations.
    
    
    import numpy as np
    import matplotlib.pyplot as plt
    import brian2 as b2
    from time import time
    
    b2.set_device('cpp_standalone', build_on_run=False)
    
    if __name__ == "__main__":
        start_time = time()
        num_inputs = 100
        input_rate = 10 * b2.Hz
        weight = 0.1
    
        net = b2.Network()
        P = b2.PoissonGroup(num_inputs, rates=input_rate)
        eqs = """
        dv/dt = -v/tau : 1
        tau : second (constant)
        """
        G = b2.NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='euler')
        S = b2.Synapses(P, G, on_pre='v += weight')
        S.connect()
        M = b2.SpikeMonitor(G)
        net.add([P, G, S, M])
    
        net.run(1000 * b2.ms)
    
        b2.device.build(run=False)  # compile the code, but don't run it yet
    
        npoints = 15
        tau_range = np.linspace(1, 15, npoints) * b2.ms
    
        output_rates = np.zeros(npoints)
        for ii in range(npoints):
            tau_i = tau_range[ii]
            b2.device.run(run_args={G.tau: tau_i})
            output_rates[ii] = M.num_spikes / b2.second
    
        print(f"Done in {time() - start_time}")
    
        plt.plot(tau_range/b2.ms, output_rates)
        plt.xlabel(r"$\tau$ (ms)")
        plt.ylabel("Firing rate (sp/s)")
        plt.show()
    

![../_images/standalone.standalone_multiplerun.1.png](../_images/standalone.standalone_multiplerun.1.png)

---

# Example: state_variables2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/synapses.state_variables.html

# Example: state_variables

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/synapses/state_variables.ipynb)

Set state variable values with a string (using code generation).
    
    
    from brian2 import *
    
    G = NeuronGroup(100, 'v:volt', threshold='v>-50*mV')
    G.v = '(sin(2*pi*i/N) - 70 + 0.25*randn()) * mV'
    S = Synapses(G, G, 'w : volt', on_pre='v += w')
    S.connect()
    
    space_constant = 200.0
    S.w['i > j'] = 'exp(-(i - j)**2/space_constant) * mV'
    
    # Generate a matrix for display
    w_matrix = np.zeros((len(G), len(G)))
    w_matrix[S.i[:], S.j[:]] = S.w[:]
    
    subplot(1, 2, 1)
    plot(G.v[:] / mV)
    xlabel('Neuron index')
    ylabel('v')
    subplot(1, 2, 2)
    imshow(w_matrix)
    xlabel('i')
    ylabel('j')
    title('Synaptic weight')
    tight_layout()
    show()
    

![../_images/synapses.state_variables.1.png](../_images/synapses.state_variables.1.png)

---

# Example: stochastic_odes2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/advanced.stochastic_odes.html

# Example: stochastic_odes

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/advanced/stochastic_odes.ipynb)

Demonstrate the correctness of the “derivative-free Milstein method” for multiplicative noise.
    
    
    from brian2 import *
    # We only get exactly the same random numbers for the exact solution and the
    # simulation if we use the numpy code generation target
    prefs.codegen.target = 'numpy'
    
    # setting a random seed makes all variants use exactly the same Wiener process
    seed = 12347
    
    X0 = 1
    mu = 0.5/second # drift
    sigma = 0.1/second #diffusion
    
    runtime = 1*second
    
    
    def simulate(method, dt):
        """
        simulate geometrical Brownian with the given method
        """
        np.random.seed(seed)
        G = NeuronGroup(1, 'dX/dt = (mu - 0.5*second*sigma**2)*X + X*sigma*xi*second**.5: 1',
                        dt=dt, method=method)
        G.X = X0
        mon = StateMonitor(G, 'X', record=True)
        net = Network(G, mon)
        net.run(runtime)
        return mon.t_[:], mon.X.flatten()
    
    
    def exact_solution(t, dt):
        """
        Return the exact solution for geometrical Brownian motion at the given
        time points
        """
        # Remove units for simplicity
        my_mu = float(mu)
        my_sigma = float(sigma)
        dt = float(dt)
        t = asarray(t)
    
        np.random.seed(seed)
        # We are calculating the values at the *start* of a time step, as when using
        # a StateMonitor. Therefore the Brownian motion starts with zero
        brownian = np.hstack([0, cumsum(sqrt(dt) * np.random.randn(len(t)-1))])
    
        return (X0 * exp((my_mu - 0.5*my_sigma**2)*(t+dt) + my_sigma*brownian))
    
    figure(1, figsize=(16, 7))
    figure(2, figsize=(16, 7))
    
    methods = ['milstein', 'heun']
    dts = [1*ms, 0.5*ms, 0.2*ms, 0.1*ms, 0.05*ms, 0.025*ms, 0.01*ms, 0.005*ms]
    
    rows = int(sqrt(len(dts)))
    cols = int(ceil(1.0 * len(dts) / rows))
    errors = dict([(method, zeros(len(dts))) for method in methods])
    for dt_idx, dt in enumerate(dts):
        print('dt: %s' % dt)
        trajectories = {}
        # Test the numerical methods
        for method in methods:
            t, trajectories[method] = simulate(method, dt)
        # Calculate the exact solution
        exact = exact_solution(t, dt)
    
        for method in methods:
            # plot the trajectories
            figure(1)
            subplot(rows, cols, dt_idx+1)
            plot(t, trajectories[method], label=method, alpha=0.75)
    
            # determine the mean absolute error
            errors[method][dt_idx] = mean(abs(trajectories[method] - exact))
            # plot the difference to the real trajectory
            figure(2)
            subplot(rows, cols, dt_idx+1)
            plot(t, trajectories[method] - exact, label=method, alpha=0.75)
    
        figure(1)
        plot(t, exact, color='gray', lw=2, label='exact', alpha=0.75)
        title('dt = %s' % str(dt))
        xticks([])
    
    figure(1)
    legend(frameon=False, loc='best')
    tight_layout()
    
    figure(2)
    legend(frameon=False, loc='best')
    tight_layout()
    
    figure(3)
    for method in methods:
        plot(array(dts) / ms, errors[method], 'o', label=method)
    legend(frameon=False, loc='best')
    xscale('log')
    yscale('log')
    xlabel('dt (ms)')
    ylabel('Mean absolute error')
    tight_layout()
    
    show()
    

![../_images/advanced.stochastic_odes.1.png](../_images/advanced.stochastic_odes.1.png) ![../_images/advanced.stochastic_odes.2.png](../_images/advanced.stochastic_odes.2.png) ![../_images/advanced.stochastic_odes.3.png](../_images/advanced.stochastic_odes.3.png)

---

# Example: synapses2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/examples/synapses.synapses.html

# Example: synapses

> Note
> 
> You can launch an interactive, editable version of this example without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=examples/synapses/synapses.ipynb)

A simple example of using [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses").
    
    
    from brian2 import *
    
    G1 = NeuronGroup(10, 'dv/dt = -v / (10*ms) : 1',
                     threshold='v > 1', reset='v=0.', method='exact')
    G1.v = 1.2
    G2 = NeuronGroup(10, 'dv/dt = -v / (10*ms) : 1',
                     threshold='v > 1', reset='v=0', method='exact')
    
    syn = Synapses(G1, G2, 'dw/dt = -w / (50*ms): 1 (event-driven)', on_pre='v += w')
    
    syn.connect('i == j', p=0.75)
    
    # Set the delays
    syn.delay = '1*ms + i*ms + 0.25*ms * randn()'
    # Set the initial values of the synaptic variable
    syn.w = 1
    
    mon = StateMonitor(G2, 'v', record=True)
    run(20*ms)
    plot(mon.t/ms, mon.v.T)
    xlabel('Time (ms)')
    ylabel('v')
    show()
    

![../_images/synapses.synapses.1.png](../_images/synapses.synapses.1.png)

---

# Functions2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/advanced/functions.html

# Functions  
  
  * Default functions

  * User-provided functions

    * Python code generation

    * Other code generation targets

    * Dependencies between functions

    * Additional compiler arguments

    * Arrays vs. scalar values in user-provided functions

    * Functions with context-dependent return values

    * Additional namespace

    * Data types

    * External source files

All equations, expressions and statements in Brian can make use of mathematical functions. However, functions have to be prepared for use with Brian for two reasons: 1) Brian is strict about checking the consistency of units, therefore every function has to specify how it deals with units; 2) functions need to be implemented differently for different code generation targets.

Brian provides a number of default functions that are already prepared for use with numpy and C++ and also provides a mechanism for preparing new functions for use (see below).

## Default functions

The following functions (stored in the `DEFAULT_FUNCTIONS` dictionary) are ready for use:

  * Random numbers: `rand` (random numbers drawn from a uniform distribution between 0 and 1), `randn` (random numbers drawn from the standard normal distribution, i.e. with mean 0 and standard deviation 1), and `poisson` (discrete random numbers from a Poisson distribution with rate parameter \\(\lambda\\))

  * Elementary functions: `sqrt`, `exp`, `log`, `log10`, `abs`, `sign`

  * Trigonometric functions: `sin`, `cos`, `tan`, `sinh`, `cosh`, `tanh`, `arcsin`, `arccos`, `arctan`

  * Functions for improved numerical accuracy: `expm1` (calculates `exp(x) - 1`, more accurate for `x` close to 0), `log1p` (calculates `log(1 + x)`, more accurate for `x` close to 0), and `exprel` (calculates `(exp(x) - 1)/x`, more accurate for `x` close to 0, and returning 1.0 instead of `NaN` for `x == 0`

  * General utility functions: `clip`, `floor`, `ceil`

Brian also provides a special purpose function `int`, which can be used to convert an expression or variable into an integer value. This is especially useful for boolean values (which will be converted into 0 or 1), for example to have a conditional evaluation as part of an equation or statement which sometimes allows to circumvent the lack of an `if` statement. For example, the following reset statement resets the variable `v` to either `v_r1` or `v_r2`, depending on the value of `w`: `'v = v_r1 * int(w <= 0.5) + v_r2 * int(w > 0.5)'`

Finally, the function [`timestep`](../reference/brian2.core.functions.timestep.html#brian2.core.functions.timestep "brian2.core.functions.timestep") is a function that takes a time and the length of a time step as an input and returns an integer corresponding to the respective time step. The advantage of using this function over a simple division is that it slightly shifts the time before dividing to avoid floating point issues. This function is used as part of the [Refractoriness](../user/refractoriness.html) mechanism.

## User-provided functions

### Python code generation

If a function is only used in contexts that use Python code generation, preparing a function for use with Brian only means specifying its units. The simplest way to do this is to use the [`check_units()`](../reference/brian2.units.fundamentalunits.check_units.html#brian2.units.fundamentalunits.check_units "brian2.units.fundamentalunits.check_units") decorator:
    
    
    @check_units(x1=meter, y1=meter, x2=meter, y2=meter, result=meter)
    def distance(x1, y1, x2, y2):
        return sqrt((x1 - x2)**2 + (y1 - y2)**2)
    

Another option is to wrap the function in a [`Function`](../reference/brian2.core.functions.Function.html#brian2.core.functions.Function "brian2.core.functions.Function") object:
    
    
    def distance(x1, y1, x2, y2):
        return sqrt((x1 - x2)**2 + (y1 - y2)**2)
    # wrap the distance function
    distance = Function(distance, arg_units=[meter, meter, meter, meter],
                        return_unit=meter)
    

The use of Brian’s unit system has the benefit of checking the consistency of units for every operation but at the expense of performance. Consider the following function, for example:
    
    
    @check_units(I=amp, result=Hz)
    def piecewise_linear(I):
        return clip((I-1*nA) * 50*Hz/nA, 0*Hz, 100*Hz)
    

When Brian runs a simulation, the state variables are stored and passed around without units for performance reasons. If the above function is used, however, Brian adds units to its input argument so that the operations inside the function do not fail with dimension mismatches. Accordingly, units are removed from the return value so that the function output can be used with the rest of the code. For better performance, Brian can alter the namespace of the function when it is executed as part of the simulation and remove all the units, then pass values without units to the function. In the above example, this means making the symbol `nA` refer to `1e-9` and `Hz` to `1`. To use this mechanism, add the decorator [`implementation()`](../reference/brian2.core.functions.implementation.html#brian2.core.functions.implementation "brian2.core.functions.implementation") with the `discard_units` keyword:
    
    
    @implementation('numpy', discard_units=True)
    @check_units(I=amp, result=Hz)
    def piecewise_linear(I):
        return clip((I-1*nA) * 50*Hz/nA, 0*Hz, 100*Hz)
    

Note that the use of the function _outside of simulation runs_ is not affected, i.e. using `piecewise_linear` still requires a current in Ampere and returns a rate in Hertz. The `discard_units` mechanism does not work in all cases, e.g. it does not work if the function refers to units as `brian2.nA` instead of `nA`, if it uses imports inside the function (e.g. `from brian2 import nA`), etc. The `discard_units` can also be switched on for all functions without having to use the [`implementation()`](../reference/brian2.core.functions.implementation.html#brian2.core.functions.implementation "brian2.core.functions.implementation") decorator by setting the [codegen.runtime.numpy.discard_units](../reference/brian2.codegen.runtime.numpy_rt.html#brian-pref-codegen-runtime-numpy-discard-units) preference.

### Other code generation targets

To make a function available for other code generation targets (e.g. C++), implementations for these targets have to be added. This can be achieved using the [`implementation()`](../reference/brian2.core.functions.implementation.html#brian2.core.functions.implementation "brian2.core.functions.implementation") decorator. The form of the code (e.g. a simple string or a dictionary of strings) necessary is target-dependent, for C++ both options are allowed, a simple string will be interpreted as filling the `'support_code'` block. Note that `'cpp'` is used to provide C++ implementations. An implementation for the C++ target could look like this:
    
    
    @implementation('cpp', '''
         double piecewise_linear(double I) {
            if (I < 1e-9)
                return 0;
            if (I > 3e-9)
                return 100;
            return (I/1e-9 - 1) * 50;
         }
         ''')
    @check_units(I=amp, result=Hz)
    def piecewise_linear(I):
        return clip((I-1*nA) * 50*Hz/nA, 0*Hz, 100*Hz)
    

Alternatively, `FunctionImplementation` objects can be added to the [`Function`](../reference/brian2.core.functions.Function.html#brian2.core.functions.Function "brian2.core.functions.Function") object.

The same sort of approach as for C++ works for Cython using the `'cython'` target. The example above would look like this:
    
    
    @implementation('cython', '''
        cdef double piecewise_linear(double I):
            if I<1e-9:
                return 0.0
            elif I>3e-9:
                return 100.0
            return (I/1e-9-1)*50
        ''')
    @check_units(I=amp, result=Hz)
    def piecewise_linear(I):
        return clip((I-1*nA) * 50*Hz/nA, 0*Hz, 100*Hz)
    

### Dependencies between functions

The code generation mechanism for user-defined functions only adds the source code for a function when it is necessary. If a user-defined function refers to another function in its source code, it therefore has to explicitly state this dependency so that the code of the dependency is added as well:
    
    
    @implementation('cpp','''
        double rectified_linear(double x)
        {
            return clip(x, 0, INFINITY);
        }''',
        dependencies={'clip': DEFAULT_FUNCTIONS['clip']}
        )
    @check_units(x=1, result=1)
    def rectified_linear(x):
        return np.clip(x, 0, np.inf)
    

Note

The dependency mechanism is unnecessary for the `numpy` code generation target, since functions are defined as actual Python functions and not as code given in a string.

### Additional compiler arguments

If the code for a function needs additional compiler options to work, e.g. to link to an external library, these options can be provided as keyword arguments to the `@implementation` decorator. E.g. to link C++ code to the `foo` library which is stored in the directory `/usr/local/foo`, use:
    
    
    @implementation('cpp', '...',
     libraries=['foo'], library_dirs=['/usr/local/foo'])
    

These arguments can also be used to refer to external source files, see below. Equivalent arguments can also be set as global [Preferences](preferences.html) in which case they apply to all code and not only to code referring to the respective function. Note that in C++ standalone mode, all files are compiled together, and therefore the additional compiler arguments provided to functions are always combined with the preferences into a common set of settings that is applied to all code.

The list of currently supported additional arguments (for further explications, see the respective [Preferences](preferences.html) and the Python documentation of the `distutils.core.Extension` class):

keyword | C++ standalone | Cython  
---|---|---  
`headers` | ✓ | ❌  
`sources` | ✓ | ✓  
`define_macros` | ✓ | ❌  
`libraries` | ✓ | ✓  
`include_dirs` | ✓ | ✓  
`library_dirs` | ✓ | ✓  
`runtime_library_dirs` | ✓ | ✓  
  
### Arrays vs. scalar values in user-provided functions

Equations, expressions and abstract code statements are always implicitly referring to all the neurons in a [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup"), all the synapses in a [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses") object, etc. Therefore, function calls also apply to more than a single value. The way in which this is handled differs between code generation targets that support vectorized expressions (e.g. the `numpy` target) and targets that don’t (e.g. the `cpp_standalone` mode). If the code generation target supports vectorized expressions, it will receive an array of values. For example, in the `piecewise_linear` example above, the argument `I` will be an array of values and the function returns an array of values. For code generation without support for vectorized expressions, all code will be executed in a loop (over neurons, over synapses, …), the function will therefore be called several times with a single value each time.

In both cases, the function will only receive the “relevant” values, meaning that if for example a function is evaluated as part of a reset statement, it will only receive values for the neurons that just spiked.

### Functions with context-dependent return values

When using the `numpy` target, functions have to return an array of values (e.g. one value for each neuron). In some cases, the number of values to return cannot be deduced from the function’s arguments. Most importantly, this is the case for random numbers: a call to `rand()` has to return one value for each neuron if it is part of a neuron’s equations, but only one value for each neuron that spiked during the time step if it is part of the reset statement. Such function are said to “auto vectorise”, which means that their implementation receives an additional array argument `_vectorisation_idx`; the length of this array determines the number of values the function should return. This argument is also provided to functions for other code generation targets, but in these cases it is a single value (e.g. the index of the neuron), and is currently ignored. To enable this property on a user-defined function, you’ll currently have to manually create a [`Function`](../reference/brian2.core.functions.Function.html#brian2.core.functions.Function "brian2.core.functions.Function") object:
    
    
    def exponential_rand(l, _vectorisation_idx):
        '''Generate a number from an exponential distribution using inverse
           transform sampling'''
        uniform = np.random.rand(len(_vectorisation_idx))
        return -(1/l)*np.log(1 - uniform)
    
    exponential_rand = Function(exponential_rand, arg_units=[1], return_unit=1,
                                stateless=False, auto_vectorise=True)
    

Implementations for other code generation targets can then be added using the `add_implementation` mechanism:
    
    
    cpp_code = '''
    double exponential_rand(double l, int _vectorisation_idx)
    {
        double uniform = rand(_vectorisation_idx);
        return -(1/l)*log(1 - uniform);
    }
    '''
    exponential_rand.implementations.add_implementation('cpp', cpp_code,
                                                        dependencies={'rand': DEFAULT_FUNCTIONS['rand'],
                                                                      'log': DEFAULT_FUNCTIONS['log']})
    

Note that by referring to the `rand` function, the new random number generator will automatically generate reproducible random numbers if the [`seed()`](../reference/brian2.devices.device.seed.html#brian2.devices.device.seed "brian2.devices.device.seed") function is use to set its seed. Restoring the random number state with [`restore()`](../reference/brian2.core.magic.restore.html#brian2.core.magic.restore "brian2.core.magic.restore") will have the expected effect as well.

### Additional namespace

Some functions need additional data to compute a result, e.g. a [`TimedArray`](../reference/brian2.input.timedarray.TimedArray.html#brian2.input.timedarray.TimedArray "brian2.input.timedarray.TimedArray") needs access to the underlying array. For the `numpy` target, a function can simply use a reference to an object defined outside the function, there is no need to explicitly pass values in a namespace. For the other code language targets, values can be passed in the `namespace` argument of the [`implementation()`](../reference/brian2.core.functions.implementation.html#brian2.core.functions.implementation "brian2.core.functions.implementation") decorator or the [`add_implementation`](../reference/brian2.core.functions.FunctionImplementationContainer.html#brian2.core.functions.FunctionImplementationContainer.add_implementation "brian2.core.functions.FunctionImplementationContainer.add_implementation") method. The namespace values are then accessible in the function code under the given name, prefixed with `_namespace`. Note that this mechanism should only be used for numpy arrays or general objects (e.g. function references to call Python functions from Cython code). Scalar values should be directly included in the function code, by using a “dynamic implemention” (see [`add_dynamic_implementation`](../reference/brian2.core.functions.FunctionImplementationContainer.html#brian2.core.functions.FunctionImplementationContainer.add_dynamic_implementation "brian2.core.functions.FunctionImplementationContainer.add_dynamic_implementation")).

See [`TimedArray`](../reference/brian2.input.timedarray.TimedArray.html#brian2.input.timedarray.TimedArray "brian2.input.timedarray.TimedArray") and [`BinomialFunction`](../reference/brian2.input.binomial.BinomialFunction.html#brian2.input.binomial.BinomialFunction "brian2.input.binomial.BinomialFunction") for examples that use this mechanism.

### Data types

By default, functions are assumed to take any type of argument, and return a floating point value. If you want to put a restriction on the type of an argument, or specify that the return type should be something other than float, either declare it as a [`Function`](../reference/brian2.core.functions.Function.html#brian2.core.functions.Function "brian2.core.functions.Function") (and see its documentation on specifying types) or use the [`declare_types()`](../reference/brian2.core.functions.declare_types.html#brian2.core.functions.declare_types "brian2.core.functions.declare_types") decorator, e.g.:
    
    
    @check_units(a=1, b=1, result=1)
    @declare_types(a='integer', result='highest')
    def f(a, b):
        return a*b
    

This is potentially important if you have functions that return integer or boolean values, because Brian’s code generation optimisation step will make some potentially incorrect simplifications if it assumes that the return type is floating point.

### External source files

Code for functions can also be provided via external files in the target language. This can be especially useful for linking to existing code without having to include it a second time in the Python script. For C++-based code generation targets (i.e. the C++ standalone mode), the external code should be in a file that is provided as an argument to the `sources` keyword, together with a header file whose name is provided to `headers` (see the note for the [codegen.cpp.headers](../reference/brian2.codegen.html#brian-pref-codegen-cpp-headers) preference about the necessary format). Since the main simulation code is compiled and executed in a different directory, you should also point the compiler towards the directory of the header file via the `include_dirs` keyword. For the same reason, use an absolute path for the source file. For example, the `piecewise_linear` function from above can be implemented with external files as follows:
    
    
    //file: piecewise_linear.h
    double piecewise_linear(double);
    
    
    
    //file: piecewise_linear.cpp
    double piecewise_linear(double I) {
        if (I < 1e-9)
            return 0;
        if (I > 3e-9)
            return 100;
        return (I/1e-9 - 1) * 50;
    }
    
    
    
    # Python script
    
    # Get the absolute directory of this Python script, the C++ files are
    # expected to be stored alongside of it
    import os
    current_dir = os.path.abspath(os.path.dirname(__file__))
    
    @implementation('cpp', '// all code in piecewise_linear.cpp',
                    sources=[os.path.join(current_dir,
                                          'piecewise_linear.cpp')],
                    headers=['"piecewise_linear.h"'],
                    include_dirs=[current_dir])
    @check_units(I=amp, result=Hz)
    def piecewise_linear(I):
        return clip((I-1*nA) * 50*Hz/nA, 0*Hz, 100*Hz)
    

For Cython, the process is very similar (see the [Cython documentation](https://cython.readthedocs.io/en/latest/src/userguide/sharing_declarations.html) for general information). The name of the header file does not need to be specified, it is expected to have the same name as the source file (except for the `.pxd` extension). The source and header files will be automatically copied to the cache directory where Cython files are compiled, they therefore have to be imported as top-level modules, regardless of whether the executed Python code is itself in a package or module.

A Cython equivalent of above’s C++ example can be written as:
    
    
    # file: piecewise_linear.pxd
    cdef double piecewise_linear(double)
    
    
    
    # file: piecewise_linear.pyx
    cdef double piecewise_linear(double I):
        if I<1e-9:
            return 0.0
        elif I>3e-9:
            return 100.0
        return (I/1e-9-1)*50
    
    
    
    # Python script
    
    # Get the absolute directory of this Python script, the Cython files
    # are expected to be stored alongside of it
    import os
    current_dir = os.path.abspath(os.path.dirname(__file__))
    
    @implementation('cython',
                    'from piecewise_linear cimport piecewise_linear',
                    sources=[os.path.join(current_dir,
                                          'piecewise_linear.pyx')])
    @check_units(I=amp, result=Hz)
    def piecewise_linear(I):
        return clip((I-1*nA) * 50*Hz/nA, 0*Hz, 100*Hz)
    

---

# How Brian works2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/advanced/how_brian_works.html

# How Brian works

In this section we will briefly cover some of the internals of how Brian works. This is included here to understand the general process that Brian goes through in running a simulation, but it will not be sufficient to understand the source code of Brian itself or to extend it to do new things. For a more detailed view of this, see the documentation in the [Developer’s guide](../developer/index.html).

## Clock-driven versus event-driven

Brian is a clock-driven simulator. This means that the simulation time is broken into an equally spaced time grid, 0, dt, 2*dt, 3*dt, …. At each time step t, the differential equations specifying the models are first integrated giving the values at time t+dt. Spikes are generated when a condition such as `v>vt` is satisfied, and spikes can only occur on the time grid.

The advantage of clock driven simulation is that it is very flexible (arbitrary differential equations can be used) and computationally efficient. However, the time grid approximation can lead to an overestimate of the amount of synchrony that is present in a network. This is usually not a problem, and can be managed by reducing the time step dt, but it can be an issue for some models.

Note that the inaccuracy introduced by the spike time approximation is of order O(dt), so the total accuracy of the simulation is of order O(dt) per time step. This means that in many cases, there is no need to use a higher order numerical integration method than forward Euler, as it will not improve the order of the error beyond O(dt). See [State update](state_update.html) for more details of numerical integration methods.

Some simulators use an event-driven method. With this method, spikes can occur at arbitrary times instead of just on the grid. This method can be more accurate than a clock-driven simulation, but it is usually substantially more computationally expensive (especially for larger networks). In addition, they are usually more restrictive in terms of the class of differential equations that can be solved.

For a review of some of the simulation strategies that have been used, see [Brette et al. 2007](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2638500/).

## Code overview

The user-visible part of Brian consists of a number of objects such as [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup"), [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses"), [`Network`](../reference/brian2.core.network.Network.html#brian2.core.network.Network "brian2.core.network.Network"), etc. These are all written in pure Python and essentially work to translate the user specified model into the computational engine. The end state of this translation is a collection of short blocks of code operating on a namespace, which are called in a sequence by the [`Network`](../reference/brian2.core.network.Network.html#brian2.core.network.Network "brian2.core.network.Network"). Examples of these short blocks of code are the “state updaters” which perform numerical integration, or the synaptic propagation step. The namespaces consist of a mapping from names to values, where the possible values can be scalar values, fixed-length or dynamically sized arrays, and functions.

## Syntax layer

The syntax layer consists of everything that is independent of the way the final simulation is computed (i.e. the language and device it is running on). This includes things like [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup"), [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses"), [`Network`](../reference/brian2.core.network.Network.html#brian2.core.network.Network "brian2.core.network.Network"), [`Equations`](../reference/brian2.equations.equations.Equations.html#brian2.equations.equations.Equations "brian2.equations.equations.Equations"), etc.

The user-visible part of this is documented fully in the [User’s guide](../user/index.html) and the [Advanced guide](index.html). In particular, things such as the analysis of equations and assignment of numerical integrators. The end result of this process, which is passed to the computational engine, is a specification of the simulation consisting of the following data:

  * A collection of variables which are scalar values, fixed-length arrays, dynamically sized arrays, and functions. These are handled by `Variable` objects detailed in [Variables and indices](../developer/variables_indices.html). Examples: each state variable of a [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") is assigned an `ArrayVariable`; the list of spike indices stored by a [`SpikeMonitor`](../reference/brian2.monitors.spikemonitor.SpikeMonitor.html#brian2.monitors.spikemonitor.SpikeMonitor "brian2.monitors.spikemonitor.SpikeMonitor") is assigned a `DynamicArrayVariable`; etc.

  * A collection of code blocks specified via an “abstract code block” and a template name. The “abstract code block” is a sequence of statements such as `v = vr` which are to be executed. In the case that say, `v` and `vr` are arrays, then the statement is to be executed for each element of the array. These abstract code blocks are either given directly by the user (in the case of neuron threshold and reset, and synaptic pre and post codes), or generated from differential equations combined with a numerical integrator. The template name is one of a small set (around 20 total) which give additional context. For example, the code block `a = b` when considered as part of a “state update” means execute that for each neuron index. In the context of a reset statement, it means execute it for each neuron index of a neuron that has spiked. Internally, these templates need to be implemented for each target language/device, but there are relatively few of them.

  * The order of execution of these code blocks, as defined by the [`Network`](../reference/brian2.core.network.Network.html#brian2.core.network.Network "brian2.core.network.Network").

## Computational engine

The computational engine covers everything from generating to running code in a particular language or on a particular device. It starts with the abstract definition of the simulation resulting from the syntax layer described above.

The computational engine is described by a `Device` object. This is used for allocating memory, generating and running code. There are two types of device, “runtime” and “standalone”. In runtime mode, everything is managed by Python, even if individual code blocks are in a different language. Memory is managed using numpy arrays (which can be passed as pointers to use in other languages). In standalone mode, the output of the process (after calling `Device.build`) is a complete source code project that handles everything, including memory management, and is independent of Python.

For both types of device, one of the key steps that works in the same way is code generation, the creation of a compilable and runnable block of code from an abstract code block and a collection of variables. This happens in two stages: first of all, the abstract code block is converted into a code snippet, which is a syntactically correct block of code in the target language, but not one that can run on its own (it doesn’t handle accessing the variables from memory, etc.). This code snippet typically represents the inner loop code. This step is handled by a `CodeGenerator` object. In some cases it will involve a syntax translation (e.g. the Python syntax `x**y` in C++ should be `pow(x, y)`). The next step is to insert this code snippet into a template to form a compilable code block. This code block is then passed to a runtime `CodeObject`. In the case of standalone mode, this doesn’t do anything, but for runtime devices it handles compiling the code and then running the compiled code block in the given namespace.

---

# How to plot functions2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/user/plotting_functions.html

# How to plot functions

Models of synapses and neurons are typically composed of a series of functions. To affirm their correct implementation a plot is often helpful.

Consider the following membrane voltage dependent Hodgkin-Huxley equations:
    
    
    from brian2 import *
    
    VT = -63*mV
    
    eq = Equations("""
    alpha_m = 0.32*(mV**-1)*4*mV/exprel((13*mV-v+VT)/(4*mV))/ms : Hz
    beta_m = 0.28*(mV**-1)*5*mV/exprel((v-VT-40*mV)/(5*mV))/ms : Hz
    alpha_h = 0.128*exp((17*mV-v+VT)/(18*mV))/ms : Hz
    beta_h = 4./(1+exp((40*mV-v+VT)/(5*mV)))/ms : Hz
    alpha_n = 0.032*(mV**-1)*5*mV/exprel((15*mV-v+VT)/(5*mV))/ms : Hz
    beta_n = .5*exp((10*mV-v+VT)/(40*mV))/ms : Hz
    tau_n = 1/(alpha_n + beta_n) : second
    tau_m = 1/(alpha_m + beta_m) : second
    tau_h = 1/(alpha_h + beta_h) : second
    """)
    

We can do the following to plot them as function of membrane voltage:
    
    
    group = NeuronGroup(100, eq + Equations("v : volt"))
    group.v = np.linspace(-100, 100, len(group))*mV
    
    plt.plot(group.v/mV, group.tau_m[:]/ms, label="tau_m")
    plt.plot(group.v/mV, group.tau_n[:]/ms, label="tau_n")
    plt.plot(group.v/mV, group.tau_h[:]/ms, label="tau_h")
    plt.xlabel('membrane voltage / mV')
    plt.ylabel('tau / ms')
    plt.legend()
    

![../_images/function_plot.png](../_images/function_plot.png)

Note that we need to use `[:]` for the `tau_...` equations, because Brian cannot resolve the external constant `VT` otherwise. Alternatively we could have supplied the constant in the namespace of the [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup"), see [Namespaces](../advanced/namespaces.html).

---

# Importing Brian2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/user/import.html

# Importing Brian

After installation, Brian is available in the `brian2` package. By doing a wildcard import from this package, i.e.:
    
    
    from brian2 import *
    

you will not only get access to the `brian2` classes and functions, but also to everything in the `pylab` package, which includes the plotting functions from [matplotlib](http://matplotlib.org/) and everything included in numpy/scipy (e.g. functions such as `arange`, `linspace`, etc.). Apart from this when you use the wildcard import, the builtin [`input`](https://docs.python.org/3/library/functions.html#input "\(in Python v3.12\)") function is overshadowed by the [`input`](https://docs.python.org/3/library/functions.html#input "\(in Python v3.12\)") module in the `brian2` package. If you wish to use the builtin [`input`](https://docs.python.org/3/library/functions.html#input "\(in Python v3.12\)") function in your program after importing the brian2 package then you can explicitly import the [`input`](https://docs.python.org/3/library/functions.html#input "\(in Python v3.12\)") function again as shown below:
    
    
    from brian2 import *
    from builtins import input
    

The following topics are not essential for beginners.

  

## Precise control over importing

If you want to use a wildcard import from Brian, but don’t want to import all the additional symbols provided by `pylab` or don’t want to overshadow the builtin [`input`](https://docs.python.org/3/library/functions.html#input "\(in Python v3.12\)") function, you can use:
    
    
    from brian2.only import *
    

Note that whenever you use something different from the most general `from brian2 import *` statement, you should be aware that Brian overwrites some numpy functions with their unit-aware equivalents (see [Units](../developer/units.html)). If you combine multiple wildcard imports, the Brian import should therefore be the last import. Similarly, you should not import and call overwritten numpy functions directly, e.g. by using `import numpy as np` followed by `np.sin` since this will not use the unit-aware versions. To make this easier, Brian provides a `brian2.numpy_` package that provides access to everything in numpy but overwrites certain functions. If you prefer to use prefixed names, the recommended way of doing the imports is therefore:
    
    
    import brian2.numpy_ as np
    import brian2.only as br2
    

Note that it is safe to use e.g. `np.sin` and `numpy.sin` after a `from brian2 import *`.

## Dependency checks

Brian will check the dependency versions during import and raise an error for an outdated dependency. An outdated dependency does not necessarily mean that Brian cannot be run with it, it only means that Brian is untested on that version. If you want to force Brian to run despite the outdated dependency, set the [core.outdated_dependency_error](../reference/brian2.core.html#brian-pref-core-outdated-dependency-error) preference to `False`. Note that this cannot be done in a script, since you do not have access to the preferences before importing `brian2`. See [Preferences](../advanced/preferences.html) for instructions how to set preferences in a file.

---

# Input stimuli2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/user/input.html

# Input stimuli

For Brian 1 users

See the document [Inputs (Brian 1 –> 2 conversion)](../introduction/brian1_to_2/inputs.html) for details how to convert Brian 1 code.

  * Poisson inputs

  * Spike generation

  * Explicit equations

  * Timed arrays

  * Regular operations

  * More on Poisson inputs

  * Arbitrary Python code (network operations)

There are various ways of providing “external” input to a network.

## Poisson inputs

For generating spikes according to a Poisson point process, [`PoissonGroup`](../reference/brian2.input.poissongroup.PoissonGroup.html#brian2.input.poissongroup.PoissonGroup "brian2.input.poissongroup.PoissonGroup") can be used, e.g.:
    
    
    P = PoissonGroup(100, np.arange(100)*Hz + 10*Hz)
    G = NeuronGroup(100, 'dv/dt = -v / (10*ms) : 1')
    S = Synapses(P, G, on_pre='v+=0.1')
    S.connect(j='i')
    

See More on Poisson inputs below for further information.

For simulations where the individually generated spikes are just used as a source of input to a neuron, the [`PoissonInput`](../reference/brian2.input.poissoninput.PoissonInput.html#brian2.input.poissoninput.PoissonInput "brian2.input.poissoninput.PoissonInput") class provides a more efficient alternative: see Efficient Poisson inputs via PoissonInput below for details.

## Spike generation

You can also generate an explicit list of spikes given via arrays using [`SpikeGeneratorGroup`](../reference/brian2.input.spikegeneratorgroup.SpikeGeneratorGroup.html#brian2.input.spikegeneratorgroup.SpikeGeneratorGroup "brian2.input.spikegeneratorgroup.SpikeGeneratorGroup"). This object behaves just like a [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") in that you can connect it to other groups via a [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses") object, but you specify three bits of information: `N` the number of neurons in the group; `indices` an array of the indices of the neurons that will fire; and `times` an array of the same length as `indices` with the times that the neurons will fire a spike. The `indices` and `times` arrays are matching, so for example `indices=[0,2,1]` and `times=[1*ms,2*ms,3*ms]` means that neuron 0 fires at time 1 ms, neuron 2 fires at 2 ms and neuron 1 fires at 3 ms. Example use:
    
    
    indices = array([0, 2, 1])
    times = array([1, 2, 3])*ms
    G = SpikeGeneratorGroup(3, indices, times)
    

The spikes that will be generated by [`SpikeGeneratorGroup`](../reference/brian2.input.spikegeneratorgroup.SpikeGeneratorGroup.html#brian2.input.spikegeneratorgroup.SpikeGeneratorGroup "brian2.input.spikegeneratorgroup.SpikeGeneratorGroup") can be changed between runs with the [`set_spikes`](../reference/brian2.input.spikegeneratorgroup.SpikeGeneratorGroup.html#brian2.input.spikegeneratorgroup.SpikeGeneratorGroup.set_spikes "brian2.input.spikegeneratorgroup.SpikeGeneratorGroup.set_spikes") method. This can be useful if the input to a system should depend on its previous output or when running multiple trials with different input:
    
    
    inp = SpikeGeneratorGroup(N, indices, times)
    G = NeuronGroup(N, '...')
    feedforward = Synapses(inp, G, '...', on_pre='...')
    feedforward.connect(j='i')
    recurrent = Synapses(G, G, '...', on_pre='...')
    recurrent.connect('i!=j')
    spike_mon = SpikeMonitor(G)
    # ...
    run(runtime)
    # Replay the previous output of group G as input into the group
    inp.set_spikes(spike_mon.i, spike_mon.t + runtime)
    run(runtime)
    

## Explicit equations

If the input can be explicitly expressed as a function of time (e.g. a sinusoidal input current), then its description can be directly included in the equations of the respective group:
    
    
    G = NeuronGroup(100, '''dv/dt = (-v + I)/(10*ms) : 1
                            rates : Hz  # each neuron's input has a different rate
                            size : 1  # and a different amplitude
                            I = size*sin(2*pi*rates*t) : 1''')
    G.rates = '10*Hz + i*Hz'
    G.size = '(100-i)/100. + 0.1'
    

## Timed arrays

If the time dependence of the input cannot be expressed in the equations in the way shown above, it is possible to create a [`TimedArray`](../reference/brian2.input.timedarray.TimedArray.html#brian2.input.timedarray.TimedArray "brian2.input.timedarray.TimedArray"). This acts as a function of time where the values at given time points are given explicitly. This can be especially useful to describe non-continuous stimulation. For example, the following code defines a [`TimedArray`](../reference/brian2.input.timedarray.TimedArray.html#brian2.input.timedarray.TimedArray "brian2.input.timedarray.TimedArray") where stimulus blocks consist of a constant current of random strength for 30ms, followed by no stimulus for 20ms. Note that in this particular example, numerical integration can use exact methods, since it can assume that the [`TimedArray`](../reference/brian2.input.timedarray.TimedArray.html#brian2.input.timedarray.TimedArray "brian2.input.timedarray.TimedArray") is a constant function of time during a single integration time step.

Note

The semantics of [`TimedArray`](../reference/brian2.input.timedarray.TimedArray.html#brian2.input.timedarray.TimedArray "brian2.input.timedarray.TimedArray") changed slightly compared to Brian 1: for `TimedArray([x1, x2, ...], dt=my_dt)`, the value `x1` will be returned for all `0<=t<my_dt`, `x2` for `my_dt<=t<2*my_dt` etc., whereas Brian1 returned `x1` for `0<=t<0.5*my_dt`, `x2` for `0.5*my_dt<=t<1.5*my_dt`, etc.
    
    
    stimulus = TimedArray(np.hstack([[c, c, c, 0, 0]
                                     for c in np.random.rand(1000)]),
                                    dt=10*ms)
    G = NeuronGroup(100, 'dv/dt = (-v + stimulus(t))/(10*ms) : 1',
                    threshold='v>1', reset='v=0')
    G.v = '0.5*rand()'  # different initial values for the neurons
    

[`TimedArray`](../reference/brian2.input.timedarray.TimedArray.html#brian2.input.timedarray.TimedArray "brian2.input.timedarray.TimedArray") can take a one-dimensional value array (as above) and therefore return the same value for all neurons or it can take a two-dimensional array with time as the first and (neuron/synapse/…-)index as the second dimension.

In the following, this is used to implement shared noise between neurons, all the “even neurons” get the first noise instantiation, all the “odd neurons” get the second:
    
    
    runtime = 1*second
    stimulus = TimedArray(np.random.rand(int(runtime/defaultclock.dt), 2),
                          dt=defaultclock.dt)
    G = NeuronGroup(100, 'dv/dt = (-v + stimulus(t, i % 2))/(10*ms) : 1',
                    threshold='v>1', reset='v=0')
    

## Regular operations

An alternative to specifying a stimulus in advance is to run explicitly specified code at certain points during a simulation. This can be achieved with [`run_regularly()`](../reference/brian2.groups.group.Group.html#brian2.groups.group.Group.run_regularly "brian2.groups.group.Group.run_regularly"). One can think of these statements as equivalent to reset statements but executed unconditionally (i.e. for all neurons) and possibly on a different clock than the rest of the group. The following code changes the stimulus strength of half of the neurons (randomly chosen) to a new random value every 50ms. Note that the statement uses logical expressions to have the values only updated for the chosen subset of neurons (where the newly introduced auxiliary variable `change` equals 1):
    
    
    G = NeuronGroup(100, '''dv/dt = (-v + I)/(10*ms) : 1
                            I : 1  # one stimulus per neuron''')
    G.run_regularly('''change = int(rand() < 0.5)
                       I = change*(rand()*2) + (1-change)*I''',
                    dt=50*ms)
    

The following topics are not essential for beginners.

  

## More on Poisson inputs

### Setting rates for Poisson inputs

`PoissonGroup` takes either a constant rate, an array of rates (one rate per neuron, as in the example above), or a string expression evaluating to a rate as an argument.

If the given value for `rates` is a constant, then using `PoissonGroup(N, rates)` is equivalent to:
    
    
    NeuronGroup(N, 'rates : Hz', threshold='rand()<rates*dt')
    

and setting the group’s `rates` attribute.

If `rates` is a string, then this is equivalent to:
    
    
    NeuronGroup(N, 'rates = ... : Hz', threshold='rand()<rates*dt')
    

with the respective expression for the rates. This expression will be evaluated at every time step and therefore allows the use of time-dependent rates, i.e. inhomogeneous Poisson processes. For example, the following code (see also Timed arrays) uses a [`TimedArray`](../reference/brian2.input.timedarray.TimedArray.html#brian2.input.timedarray.TimedArray "brian2.input.timedarray.TimedArray") to define the rates of a [`PoissonGroup`](../reference/brian2.input.poissongroup.PoissonGroup.html#brian2.input.poissongroup.PoissonGroup "brian2.input.poissongroup.PoissonGroup") as a function of time, resulting in five 100ms blocks of 100 Hz stimulation, followed by 100ms of silence:
    
    
    stimulus = TimedArray(np.tile([100., 0.], 5)*Hz, dt=100.*ms)
    P = PoissonGroup(1, rates='stimulus(t)')
    

Note that, as can be seen in its equivalent [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") formulation, a [`PoissonGroup`](../reference/brian2.input.poissongroup.PoissonGroup.html#brian2.input.poissongroup.PoissonGroup "brian2.input.poissongroup.PoissonGroup") does not work for high rates where more than one spike might fall into a single timestep. Use several units with lower rates in this case (e.g. use `PoissonGroup(10, 1000*Hz)` instead of `PoissonGroup(1, 10000*Hz)`).

### Efficient Poisson inputs via PoissonInput

For simulations where the [`PoissonGroup`](../reference/brian2.input.poissongroup.PoissonGroup.html#brian2.input.poissongroup.PoissonGroup "brian2.input.poissongroup.PoissonGroup") is just used as a source of input to a neuron (i.e., the individually generated spikes are not important, just their impact on the target cell), the [`PoissonInput`](../reference/brian2.input.poissoninput.PoissonInput.html#brian2.input.poissoninput.PoissonInput "brian2.input.poissoninput.PoissonInput") class provides a more efficient alternative: instead of generating spikes, [`PoissonInput`](../reference/brian2.input.poissoninput.PoissonInput.html#brian2.input.poissoninput.PoissonInput "brian2.input.poissoninput.PoissonInput") directly updates a target variable based on the sum of independent Poisson processes:
    
    
    G = NeuronGroup(100, 'dv/dt = -v / (10*ms) : 1')
    P = PoissonInput(G, 'v', 100, 100*Hz, weight=0.1)
    

Each input of the [`PoissonInput`](../reference/brian2.input.poissoninput.PoissonInput.html#brian2.input.poissoninput.PoissonInput "brian2.input.poissoninput.PoissonInput") is connected to all the neurons of the target [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") but each neuron receives independent realizations of the Poisson spike trains. Note that the [`PoissonInput`](../reference/brian2.input.poissoninput.PoissonInput.html#brian2.input.poissoninput.PoissonInput "brian2.input.poissoninput.PoissonInput") class is however more restrictive than [`PoissonGroup`](../reference/brian2.input.poissongroup.PoissonGroup.html#brian2.input.poissongroup.PoissonGroup "brian2.input.poissongroup.PoissonGroup"), it only allows for a constant rate across all neurons (but you can create several [`PoissonInput`](../reference/brian2.input.poissoninput.PoissonInput.html#brian2.input.poissoninput.PoissonInput "brian2.input.poissoninput.PoissonInput") objects, targeting different subgroups). It internally uses [`BinomialFunction`](../reference/brian2.input.binomial.BinomialFunction.html#brian2.input.binomial.BinomialFunction "brian2.input.binomial.BinomialFunction") which will draw a random number each time step, either from a binomial distribution or from a normal distribution as an approximation to the binomial distribution if \\(n p > 5 \wedge n (1 - p) > 5\\) , where \\(n\\) is the number of inputs and \\(p = dt \cdot rate\\) the spiking probability for a single input.

## Arbitrary Python code (network operations)

If none of the above techniques is general enough to fulfill the requirements of a simulation, Brian allows you to write a [`NetworkOperation`](../reference/brian2.core.operations.NetworkOperation.html#brian2.core.operations.NetworkOperation "brian2.core.operations.NetworkOperation"), an arbitrary Python function that is executed every time step (possible on a different clock than the rest of the simulation). This function can do arbitrary operations, use conditional statements etc. and it will be executed as it is (i.e. as pure Python code even if cython code generation is active). Note that one cannot use network operations in combination with the C++ standalone mode. Network operations are particularly useful when some condition or calculation depends on operations across neurons, which is currently not possible to express in abstract code. The following code switches input on for a randomly chosen single neuron every 50 ms:
    
    
    G = NeuronGroup(10, '''dv/dt = (-v + active*I)/(10*ms) : 1
                           I = sin(2*pi*100*Hz*t) : 1 (shared) #single input
                           active : 1  # will be set in the network operation''')
    @network_operation(dt=50*ms)
    def update_active():
        index = np.random.randint(10)  # index for the active neuron
        G.active_ = 0  # the underscore switches off unit checking
        G.active_[index] = 1
    

Note that the network operation (in the above example: `update_active`) has to be included in the [`Network`](../reference/brian2.core.network.Network.html#brian2.core.network.Network "brian2.core.network.Network") object if one is constructed explicitly.

Only functions with zero or one arguments can be used as a [`NetworkOperation`](../reference/brian2.core.operations.NetworkOperation.html#brian2.core.operations.NetworkOperation "brian2.core.operations.NetworkOperation"). If the function has one argument then it will be passed the current time `t`:
    
    
    @network_operation(dt=1*ms)
    def update_input(t):
        if t>50*ms and t<100*ms:
            pass # do something
    

Note that this is preferable to accessing `defaultclock.t` from within the function – if the network operation is not running on the [`defaultclock`](../reference/brian2.core.clocks.defaultclock.html#brian2.core.clocks.defaultclock "brian2.core.clocks.defaultclock") itself, then that value is not guaranteed to be correct.

Instance methods can be used as network operations as well, however in this case they have to be constructed explicitly, the [`network_operation()`](../reference/brian2.core.operations.network_operation.html#brian2.core.operations.network_operation "brian2.core.operations.network_operation") decorator cannot be used:
    
    
    class Simulation(object):
        def __init__(self, data):
            self.data = data
            self.group = NeuronGroup(...)
            self.network_op = NetworkOperation(self.update_func, dt=10*ms)
            self.network = Network(self.group, self.network_op)
    
        def update_func(self):
            pass # do something
    
        def run(self, runtime):
            self.network.run(runtime)
    

---

# Installation2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/introduction/install.html

# Installation

  * Standard install

  * Updating an existing installation

  * Requirements for C++ code generation

  * Development install

  * Installing other useful packages

  * Testing Brian

There are various ways to install Brian, and we recommend that you chose the installation method that they are most familiar with and use for other Python packages. If you do not yet have Python installed on your system (in particular on Windows machines), you can install Python and all of Brian’s dependencies via the [Anaconda distribution](https://www.anaconda.com/distribution/#download-section). You can then install Brian with the `conda` package manager as detailed below.

Note

You need to have access to Python >=3.7 (see Brian’s [support policy](compatibility.html#supported-python)). In particular, Brian no longer supports Python 2 (the last version to support Python 2 was [Brian 2.3](release_notes.html#brian2-3)). All provided Python packages also require a 64 bit system, but every desktop or laptop machine built in the last 10 years (and even most older machines) is 64 bit compatible.

If you are relying on Python packages for several, independent projects, we recommend that you make use of separate environments for each project. In this way, you can safely update and install packages for one of your projects without affecting the others. Both, `conda` and `pip` support installation in environments – for more explanations see the respective instructions below.

## Standard install

conda packagePyPI package (`pip`)Ubuntu/Debian packageFedora packageSpack package

We recommend installing Brian into a separate environment, see [conda’s documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) for more details. Brian 2 is not part of the main Anaconda distribution, but built using the community-maintained [conda-forge](https://conda-forge.org/) project. You will therefore have to to install it from the [conda-forge channel](https://anaconda.org/conda-forge). To do so, use:
    
    
    conda install -c conda-forge brian2
    

You can also permanently add the channel to your list of channels:
    
    
    conda config --add channels conda-forge
    

This has only to be done once. After that, you can install and update the brian2 packages as any other Anaconda package:
    
    
    conda install brian2
    

We recommend installing Brian into a separate “virtual environment”, see the [Python Packaging User Guide](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) for more information. Brian is included in the PyPI package index: <https://pypi.python.org/pypi/Brian2> You can therefore install it with the `pip` utility:
    
    
    python -m pip install brian2
    

In rare cases where your current environment does not have access to the `pip` utility, you first have to install `pip` via:
    
    
    python -m ensurepip
    

If you are using a recent [Debian](https://debian.org)-based Linux distribution (Debian itself, or one if its derivatives like [Ubuntu](https://ubuntu.com) or [Linux Mint](https://linuxmint.com/)), you can install Brian using its built-in package manager:
    
    
    sudo apt install python3-brian
    

Brian releases get packaged by the [Debian Med](https://www.debian.org/devel/debian-med/) team, but note that it might take a while until the most recent version shows up in the repository.

If you are using [Fedora Linux](https://getfedora.org/), you can install Brian using its built-in package manager:
    
    
    sudo dnf install python-brian2
    

Brian releases get packaged by the [NeuroFedora](https://docs.fedoraproject.org/en-US/neurofedora/overview/) team, but note that it might take a while until the most recent version shows up in the repository.

[Spack](https://spack.io) is a flexible package manager supporting multiple versions, configurations, platforms, and compilers.

After setting up Spack you can install Brian with the following command:
    
    
    spack install py-brian2
    

## Updating an existing installation

How to update Brian to a new version depends on the installation method you used previously. Typically, you can run the same command that you used for installation (sometimes with an additional option to enforce an upgrade, if available):

conda packagePyPI package (`pip`)Ubuntu/Debian packageFedora package

Depending on whether you added the `conda-forge` channel to the list of channels or not (see above), you either have to include it in the update command again or can leave it away. I.e. use:
    
    
    conda update -c conda-forge brian2
    

if you did not add the channel, or:
    
    
    conda update brian2
    

if you did.

Use the install command together with the `--upgrade` or `-U` option:
    
    
    python -m pip install -U brian2
    

Update the package repository and ask for an install. Note that the package will also be updated automatically with commands like `sudo apt full-upgrade`:
    
    
    sudo apt update
    sudo apt install python3-brian
    

Update the package repository (not necessary in general, since it will be updated regularly without asking for it), and ask for an update. Note that the package will also be updated automatically with commands like `sudo dnf upgrade`:
    
    
    sudo dnf check-update python-brian2
    sudo dnf upgrade python-brian2
    

## Requirements for C++ code generation

C++ code generation is highly recommended since it can drastically increase the speed of simulations (see [Computational methods and efficiency](../user/computation.html) for details). To use it, you need a C++ compiler and [Cython](http://cython.org/) (automatically installed as a dependency of Brian).

Linux and OS XWindows

On Linux and Mac OS X, the conda package will automatically install a C++ compiler. But even if you install Brian in a different way, you will most likely already have a working C++ compiler installed on your system (try calling `g++ --version` in a terminal). If not, use your distribution’s package manager to install a `g++` package.

On Windows, [Runtime code generation](../user/computation.html#runtime) (i.e. Cython) requires the Visual Studio compiler, but you do not need a full Visual Studio installation, installing the much smaller “Build Tools” package is sufficient:

  * Install the [Microsoft Build Tools for Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

  * In Build tools, install C++ build tools and ensure the latest versions of MSVCv… build tools and Windows 10 SDK are checked.

  * Make sure that your `setuptools` package has at least version 34.4.0 (use `conda update setuptools` when using Anaconda, or `python -m pip install --upgrade setuptools` when using pip).

For [Standalone code generation](../user/computation.html#cpp-standalone), you can either use the compiler installed above or any other version of Visual Studio.

Try running the test suite (see Installing other useful packages below) after the installation to make sure everything is working as expected.

## Development install

When you encounter a problem in Brian, we will sometimes ask you to install Brian’s latest development version, which includes changes that were included after its last release.

We regularly upload the latest development version of Brian to PyPI’s test server. You can install it via:
    
    
    python -m pip install --upgrade --pre -i https://test.pypi.org/simple/ Brian2
    

Note that this requires that you already have all of Brian’s dependencies installed.

If you have `git` installed, you can also install directly from github:
    
    
    python -m pip install git+https://github.com/brian-team/brian2.git
    

Finally, in particular if you want to either contribute to Brian’s development or regularly test its latest development version, you can directly clone the git repository at github (<https://github.com/brian-team/brian2>) and then run `pip install -e .`, to install Brian in “development mode”. With this installation, updating the git repository is in general enough to keep up with changes in the code, i.e. it is not necessary to install it again.

## Installing other useful packages

There are various packages that are useful but not necessary for working with Brian. These include: [matplotlib](http://matplotlib.org/) (for plotting), [pytest](https://docs.pytest.org/en/stable/) (for running the test suite), [ipython](http://ipython.org/) and [jupyter](http://jupyter.org/)-notebook (for an interactive console).

conda packagePyPI package (`pip`)
    
    
    conda install matplotlib pytest ipython notebook
    
    
    
    python -m pip install matplotlib pytest ipython notebook
    

You should also have a look at the [brian2tools](https://brian2tools.readthedocs.io) package, which contains several useful functions to visualize Brian 2 simulations and recordings.

conda packagePyPI package (`pip`)

As of now, `brian2tools` is not yet included in the `conda-forge` channel, you therefore have to install it from our own `brian-team` channel:
    
    
    conda install -c brian-team brian2tools
    
    
    
    python -m pip install brian2tools
    

## Testing Brian

If you have the [pytest](https://docs.pytest.org/en/stable/) testing utility installed, you can run Brian’s test suite:
    
    
    import brian2
    brian2.test()
    

It should end with “OK”, showing a number of skipped tests but no errors or failures. For more control about the tests that are run see the [developer documentation on testing](../developer/guidelines/testing.html).

---

# Interfacing with external code2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/advanced/interface.html

# Interfacing with external code

Some neural simulations benefit from a direct connections to external libraries, e.g. to support real-time input from a sensor (but note that Brian currently does not offer facilities to assure real-time processing) or to perform complex calculations during a simulation run.

If the external library is written in Python (or is a library with Python bindings), then the connection can be made either using the mechanism for [User-provided functions](functions.html#user-functions), or using a [network operation](../user/input.html#network-operation).

In case of C/C++ libraries, only the [User-provided functions](functions.html#user-functions) mechanism can be used. On the other hand, such simulations can use the same user-provided C++ code to run with the [Standalone code generation](../user/computation.html#cpp-standalone) mode. In addition to that code, one generally needs to include additional header files and use compiler/linker options to interface with the external code. For this, several preferences can be used that will be taken into account for `cython` and the `cpp_standalone` device. These preferences are mostly equivalent to the respective keyword arguments for Python’s `distutils.core.Extension` class, see the documentation of the [`cpp_prefs`](../reference/brian2.codegen.html#module-brian2.codegen.cpp_prefs "brian2.codegen.cpp_prefs") module for more details.

---

# Introduction to Brian part 1: Neurons2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/resources/tutorials/1-intro-to-brian-neurons.html

# Introduction to Brian part 1: Neurons

Note

This tutorial is a static non-editable version. You can launch an interactive, editable version without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=tutorials/1-intro-to-brian-neurons.ipynb)

Alternatively, you can download a copy of the notebook file to use locally: [`1-intro-to-brian-neurons.ipynb`](../../_downloads/d7b13492f17ebfd4a976a5406d818bae/1-intro-to-brian-neurons.ipynb)

See the [tutorial overview page](index.html) for more details.

All Brian scripts start with the following. If you’re trying this notebook out in the Jupyter notebook, you should start by running this cell.
    
    
    from brian2 import *
    

Later we’ll do some plotting in the notebook, so we activate inline plotting in the notebook by doing this:
    
    
    %matplotlib inline
    

If you are not using the Jupyter notebook to run this example (e.g. you are using a standard Python terminal, or you copy&paste these example into an editor and run them as a script), then plots will not automatically be displayed. In this case, call the `show()` command explicitly after the plotting commands.

## Units system

Brian has a system for using quantities with physical dimensions:
    
    
    20*volt
    

\\[20.0\,\mathrm{V}\\]

All of the basic SI units can be used (volt, amp, etc.) along with all the standard prefixes (m=milli, p=pico, etc.), as well as a few special abbreviations like `mV` for millivolt, `pF` for picofarad, etc.
    
    
    1000*amp
    

\\[1.0\,\mathrm{k}\,\mathrm{A}\\]
    
    
    1e6*volt
    

\\[1.0\,\mathrm{M}\,\mathrm{V}\\]
    
    
    1000*namp
    

\\[1.0000000000000002\,\mathrm{\mu}\,\mathrm{A}\\]

Also note that combinations of units with work as expected:
    
    
    10*nA*5*Mohm
    

\\[49.99999999999999\,\mathrm{m}\,\mathrm{V}\\]

And if you try to do something wrong like adding amps and volts, what happens?
    
    
    5*amp+10*volt
    
    
    
    ---------------------------------------------------------------------------
    
    DimensionMismatchError                    Traceback (most recent call last)
    
    <ipython-input-8-245c0c0332d1> in <module>
    ----> 1 5*amp+10*volt
    
    
    ~/programming/brian2/brian2/units/fundamentalunits.py in __add__(self, other)
       1429
       1430     def __add__(self, other):
    -> 1431         return self._binary_operation(other, operator.add,
       1432                                       fail_for_mismatch=True,
       1433                                       operator_str='+')
    
    
    ~/programming/brian2/brian2/units/fundamentalunits.py in _binary_operation(self, other, operation, dim_operation, fail_for_mismatch, operator_str, inplace)
       1369                 message = ('Cannot calculate {value1} %s {value2}, units do not '
       1370                            'match') % operator_str
    -> 1371                 _, other_dim = fail_for_dimension_mismatch(self, other, message,
       1372                                                            value1=self,
       1373                                                            value2=other)
    
    
    ~/programming/brian2/brian2/units/fundamentalunits.py in fail_for_dimension_mismatch(obj1, obj2, error_message, **error_quantities)
        184             raise DimensionMismatchError(error_message, dim1)
        185         else:
    --> 186             raise DimensionMismatchError(error_message, dim1, dim2)
        187     else:
        188         return dim1, dim2
    
    
    DimensionMismatchError: Cannot calculate 5. A + 10. V, units do not match (units are A and V).
    

If you haven’t see an error message in Python before that can look a bit overwhelming, but it’s actually quite simple and it’s important to know how to read these because you’ll probably see them quite often.

You should start at the bottom and work up. The last line gives the error type `DimensionMismatchError` along with a more specific message (in this case, you were trying to add together two quantities with different SI units, which is impossible).

Working upwards, each of the sections starts with a filename (e.g. `C:\Users\Dan\...`) with possibly the name of a function, and then a few lines surrounding the line where the error occurred (which is identified with an arrow).

The last of these sections shows the place in the function where the error actually happened. The section above it shows the function that called that function, and so on until the first section will be the script that you actually run. This sequence of sections is called a traceback, and is helpful in debugging.

If you see a traceback, what you want to do is start at the bottom and scan up the sections until you find your own file because that’s most likely where the problem is. (Of course, your code might be correct and Brian may have a bug in which case, please let us know on the email support list.)

## A simple model

Let’s start by defining a simple neuron model. In Brian, all models are defined by systems of differential equations. Here’s a simple example of what that looks like:
    
    
    tau = 10*ms
    eqs = '''
    dv/dt = (1-v)/tau : 1
    '''
    

In Python, the notation `'''` is used to begin and end a multi-line string. So the equations are just a string with one line per equation. The equations are formatted with standard mathematical notation, with one addition. At the end of a line you write `: unit` where `unit` is the SI unit of that variable. Note that this is not the unit of the two sides of the equation (which would be `1/second`), but the unit of the _variable_ defined by the equation, i.e. in this case \\(v\\).

Now let’s use this definition to create a neuron.
    
    
    G = NeuronGroup(1, eqs)
    

In Brian, you only create groups of neurons, using the class `NeuronGroup`. The first two arguments when you create one of these objects are the number of neurons (in this case, 1) and the defining differential equations.

Let’s see what happens if we didn’t put the variable `tau` in the equation:
    
    
    eqs = '''
    dv/dt = 1-v : 1
    '''
    G = NeuronGroup(1, eqs)
    run(100*ms)
    
    
    
    ---------------------------------------------------------------------------
    
    DimensionMismatchError                    Traceback (most recent call last)

    BrianObjectException: Original error and traceback:
    Traceback (most recent call last):
      File "/home/marcel/programming/brian2/brian2/equations/equations.py", line 956, in check_units
        check_dimensions(str(eq.expr), self.dimensions[var] / second.dim,
      File "/home/marcel/programming/brian2/brian2/equations/unitcheck.py", line 45, in check_dimensions
        fail_for_dimension_mismatch(expr_dims, dimensions, err_msg)
      File "/home/marcel/programming/brian2/brian2/units/fundamentalunits.py", line 184, in fail_for_dimension_mismatch
        raise DimensionMismatchError(error_message, dim1)
    brian2.units.fundamentalunits.DimensionMismatchError: Expression 1-v does not have the expected unit hertz (unit is 1).
    
    During handling of the above exception, another exception occurred:
    
    Traceback (most recent call last):
      File "/home/marcel/programming/brian2/brian2/core/network.py", line 898, in before_run
        obj.before_run(run_namespace)
      File "/home/marcel/programming/brian2/brian2/groups/neurongroup.py", line 884, in before_run
        self.equations.check_units(self, run_namespace=run_namespace)
      File "/home/marcel/programming/brian2/brian2/equations/equations.py", line 959, in check_units
        raise DimensionMismatchError(('Inconsistent units in '
    brian2.units.fundamentalunits.DimensionMismatchError: Inconsistent units in differential equation defining variable v:
    Expression 1-v does not have the expected unit hertz (unit is 1).
    
    Error encountered with object named "neurongroup_1".
    Object was created here (most recent call only, full details in debug log):
      File "<ipython-input-11-97ed109f5888>", line 4, in <module>
        G = NeuronGroup(1, eqs)
    
    An error occurred when preparing an object. brian2.units.fundamentalunits.DimensionMismatchError: Inconsistent units in differential equation defining variable v:
    Expression 1-v does not have the expected unit hertz (unit is 1).
    (See above for original error message and traceback.)
    

An error is raised, but why? The reason is that the differential equation is now dimensionally inconsistent. The left hand side `dv/dt` has units of `1/second` but the right hand side `1-v` is dimensionless. People often find this behaviour of Brian confusing because this sort of equation is very common in mathematics. However, for quantities with physical dimensions it is incorrect because the results would change depending on the unit you measured it in. For time, if you measured it in seconds the same equation would behave differently to how it would if you measured time in milliseconds. To avoid this, we insist that you always specify dimensionally consistent equations.

Now let’s go back to the good equations and actually run the simulation.
    
    
    start_scope()
    
    tau = 10*ms
    eqs = '''
    dv/dt = (1-v)/tau : 1
    '''
    
    G = NeuronGroup(1, eqs)
    run(100*ms)
    
    
    
    INFO       No numerical integration method specified for group 'neurongroup', using method 'exact' (took 0.02s). [brian2.stateupdaters.base.method_choice]
    

First off, ignore that `start_scope()` at the top of the cell. You’ll see that in each cell in this tutorial where we run a simulation. All it does is make sure that any Brian objects created before the function is called aren’t included in the next run of the simulation.

Secondly, you’ll see that there is an “INFO” message about not specifying the numerical integration method. This is harmless and just to let you know what method we chose, but we’ll fix it in the next cell by specifying the method explicitly.

So, what has happened here? Well, the command `run(100*ms)` runs the simulation for 100 ms. We can see that this has worked by printing the value of the variable `v` before and after the simulation.
    
    
    start_scope()
    
    G = NeuronGroup(1, eqs, method='exact')
    print('Before v = %s' % G.v[0])
    run(100*ms)
    print('After v = %s' % G.v[0])
    
    
    
    Before v = 0.0
    After v = 0.9999546000702376
    

By default, all variables start with the value 0. Since the differential equation is `dv/dt=(1-v)/tau` we would expect after a while that `v` would tend towards the value 1, which is just what we see. Specifically, we’d expect `v` to have the value `1-exp(-t/tau)`. Let’s see if that’s right.
    
    
    print('Expected value of v = %s' % (1-exp(-100*ms/tau)))
    
    
    
    Expected value of v = 0.9999546000702375
    

Good news, the simulation gives the value we’d expect!

Now let’s take a look at a graph of how the variable `v` evolves over time.
    
    
    start_scope()
    
    G = NeuronGroup(1, eqs, method='exact')
    M = StateMonitor(G, 'v', record=True)
    
    run(30*ms)
    
    plot(M.t/ms, M.v[0])
    xlabel('Time (ms)')
    ylabel('v');
    

![../../_images/1-intro-to-brian-neurons_image_31_0.png](../../_images/1-intro-to-brian-neurons_image_31_0.png)

This time we only ran the simulation for 30 ms so that we can see the behaviour better. It looks like it’s behaving as expected, but let’s just check that analytically by plotting the expected behaviour on top.
    
    
    start_scope()
    
    G = NeuronGroup(1, eqs, method='exact')
    M = StateMonitor(G, 'v', record=0)
    
    run(30*ms)
    
    plot(M.t/ms, M.v[0], 'C0', label='Brian')
    plot(M.t/ms, 1-exp(-M.t/tau), 'C1--',label='Analytic')
    xlabel('Time (ms)')
    ylabel('v')
    legend();
    

![../../_images/1-intro-to-brian-neurons_image_33_0.png](../../_images/1-intro-to-brian-neurons_image_33_0.png)

As you can see, the blue (Brian) and dashed orange (analytic solution) lines coincide.

In this example, we used the object `StateMonitor` object. This is used to record the values of a neuron variable while the simulation runs. The first two arguments are the group to record from, and the variable you want to record from. We also specify `record=0`. This means that we record all values for neuron 0. We have to specify which neurons we want to record because in large simulations with many neurons it usually uses up too much RAM to record the values of all neurons.

Now try modifying the equations and parameters and see what happens in the cell below.
    
    
    start_scope()
    
    tau = 10*ms
    eqs = '''
    dv/dt = (sin(2*pi*100*Hz*t)-v)/tau : 1
    '''
    
    # Change to Euler method because exact integrator doesn't work here
    G = NeuronGroup(1, eqs, method='euler')
    M = StateMonitor(G, 'v', record=0)
    
    G.v = 5 # initial value
    
    run(60*ms)
    
    plot(M.t/ms, M.v[0])
    xlabel('Time (ms)')
    ylabel('v');
    

![../../_images/1-intro-to-brian-neurons_image_35_0.png](../../_images/1-intro-to-brian-neurons_image_35_0.png)

## Adding spikes

So far we haven’t done anything neuronal, just played around with differential equations. Now let’s start adding spiking behaviour.
    
    
    start_scope()
    
    tau = 10*ms
    eqs = '''
    dv/dt = (1-v)/tau : 1
    '''
    
    G = NeuronGroup(1, eqs, threshold='v>0.8', reset='v = 0', method='exact')
    
    M = StateMonitor(G, 'v', record=0)
    run(50*ms)
    plot(M.t/ms, M.v[0])
    xlabel('Time (ms)')
    ylabel('v');
    

![../../_images/1-intro-to-brian-neurons_image_37_0.png](../../_images/1-intro-to-brian-neurons_image_37_0.png)

We’ve added two new keywords to the `NeuronGroup` declaration: `threshold='v>0.8'` and `reset='v = 0'`. What this means is that when `v>0.8` we fire a spike, and immediately reset `v = 0` after the spike. We can put any expression and series of statements as these strings.

As you can see, at the beginning the behaviour is the same as before until `v` crosses the threshold `v>0.8` at which point you see it reset to 0. You can’t see it in this figure, but internally Brian has registered this event as a spike. Let’s have a look at that.
    
    
    start_scope()
    
    G = NeuronGroup(1, eqs, threshold='v>0.8', reset='v = 0', method='exact')
    
    spikemon = SpikeMonitor(G)
    
    run(50*ms)
    
    print('Spike times: %s' % spikemon.t[:])
    
    
    
    Spike times: [16.  32.1 48.2] ms
    

The `SpikeMonitor` object takes the group whose spikes you want to record as its argument and stores the spike times in the variable `t`. Let’s plot those spikes on top of the other figure to see that it’s getting it right.
    
    
    start_scope()
    
    G = NeuronGroup(1, eqs, threshold='v>0.8', reset='v = 0', method='exact')
    
    statemon = StateMonitor(G, 'v', record=0)
    spikemon = SpikeMonitor(G)
    
    run(50*ms)
    
    plot(statemon.t/ms, statemon.v[0])
    for t in spikemon.t:
        axvline(t/ms, ls='--', c='C1', lw=3)
    xlabel('Time (ms)')
    ylabel('v');
    

![../../_images/1-intro-to-brian-neurons_image_41_0.png](../../_images/1-intro-to-brian-neurons_image_41_0.png)

Here we’ve used the `axvline` command from `matplotlib` to draw an orange, dashed vertical line at the time of each spike recorded by the `SpikeMonitor`.

Now try changing the strings for `threshold` and `reset` in the cell above to see what happens.

## Refractoriness

A common feature of neuron models is refractoriness. This means that after the neuron fires a spike it becomes refractory for a certain duration and cannot fire another spike until this period is over. Here’s how we do that in Brian.
    
    
    start_scope()
    
    tau = 10*ms
    eqs = '''
    dv/dt = (1-v)/tau : 1 (unless refractory)
    '''
    
    G = NeuronGroup(1, eqs, threshold='v>0.8', reset='v = 0', refractory=5*ms, method='exact')
    
    statemon = StateMonitor(G, 'v', record=0)
    spikemon = SpikeMonitor(G)
    
    run(50*ms)
    
    plot(statemon.t/ms, statemon.v[0])
    for t in spikemon.t:
        axvline(t/ms, ls='--', c='C1', lw=3)
    xlabel('Time (ms)')
    ylabel('v');
    

![../../_images/1-intro-to-brian-neurons_image_44_0.png](../../_images/1-intro-to-brian-neurons_image_44_0.png)

As you can see in this figure, after the first spike, `v` stays at 0 for around 5 ms before it resumes its normal behaviour. To do this, we’ve done two things. Firstly, we’ve added the keyword `refractory=5*ms` to the `NeuronGroup` declaration. On its own, this only means that the neuron cannot spike in this period (see below), but doesn’t change how `v` behaves. In order to make `v` stay constant during the refractory period, we have to add `(unless refractory)` to the end of the definition of `v` in the differential equations. What this means is that the differential equation determines the behaviour of `v` unless it’s refractory in which case it is switched off.

Here’s what would happen if we didn’t include `(unless refractory)`. Note that we’ve also decreased the value of `tau` and increased the length of the refractory period to make the behaviour clearer.
    
    
    start_scope()
    
    tau = 5*ms
    eqs = '''
    dv/dt = (1-v)/tau : 1
    '''
    
    G = NeuronGroup(1, eqs, threshold='v>0.8', reset='v = 0', refractory=15*ms, method='exact')
    
    statemon = StateMonitor(G, 'v', record=0)
    spikemon = SpikeMonitor(G)
    
    run(50*ms)
    
    plot(statemon.t/ms, statemon.v[0])
    for t in spikemon.t:
        axvline(t/ms, ls='--', c='C1', lw=3)
    axhline(0.8, ls=':', c='C2', lw=3)
    xlabel('Time (ms)')
    ylabel('v')
    print("Spike times: %s" % spikemon.t[:])
    
    
    
    Spike times: [ 8. 23. 38.] ms
    

![../../_images/1-intro-to-brian-neurons_image_46_1.png](../../_images/1-intro-to-brian-neurons_image_46_1.png)

So what’s going on here? The behaviour for the first spike is the same: `v` rises to 0.8 and then the neuron fires a spike at time 8 ms before immediately resetting to 0. Since the refractory period is now 15 ms this means that the neuron won’t be able to spike again until time 8 + 15 = 23 ms. Immediately after the first spike, the value of `v` now instantly starts to rise because we didn’t specify `(unless refractory)` in the definition of `dv/dt`. However, once it reaches the value 0.8 (the dashed green line) at time roughly 8 ms it doesn’t fire a spike even though the threshold is `v>0.8`. This is because the neuron is still refractory until time 23 ms, at which point it fires a spike.

Note that you can do more complicated and interesting things with refractoriness. See the full documentation for more details about how it works.

## Multiple neurons

So far we’ve only been working with a single neuron. Let’s do something interesting with multiple neurons.
    
    
    start_scope()
    
    N = 100
    tau = 10*ms
    eqs = '''
    dv/dt = (2-v)/tau : 1
    '''
    
    G = NeuronGroup(N, eqs, threshold='v>1', reset='v=0', method='exact')
    G.v = 'rand()'
    
    spikemon = SpikeMonitor(G)
    
    run(50*ms)
    
    plot(spikemon.t/ms, spikemon.i, '.k')
    xlabel('Time (ms)')
    ylabel('Neuron index');
    

![../../_images/1-intro-to-brian-neurons_image_49_0.png](../../_images/1-intro-to-brian-neurons_image_49_0.png)

This shows a few changes. Firstly, we’ve got a new variable `N` determining the number of neurons. Secondly, we added the statement `G.v = 'rand()'` before the run. What this does is initialise each neuron with a different uniform random value between 0 and 1. We’ve done this just so each neuron will do something a bit different. The other big change is how we plot the data in the end.

As well as the variable `spikemon.t` with the times of all the spikes, we’ve also used the variable `spikemon.i` which gives the corresponding neuron index for each spike, and plotted a single black dot with time on the x-axis and neuron index on the y-value. This is the standard “raster plot” used in neuroscience.

## Parameters

To make these multiple neurons do something more interesting, let’s introduce per-neuron parameters that don’t have a differential equation attached to them.
    
    
    start_scope()
    
    N = 100
    tau = 10*ms
    v0_max = 3.
    duration = 1000*ms
    
    eqs = '''
    dv/dt = (v0-v)/tau : 1 (unless refractory)
    v0 : 1
    '''
    
    G = NeuronGroup(N, eqs, threshold='v>1', reset='v=0', refractory=5*ms, method='exact')
    M = SpikeMonitor(G)
    
    G.v0 = 'i*v0_max/(N-1)'
    
    run(duration)
    
    figure(figsize=(12,4))
    subplot(121)
    plot(M.t/ms, M.i, '.k')
    xlabel('Time (ms)')
    ylabel('Neuron index')
    subplot(122)
    plot(G.v0, M.count/duration)
    xlabel('v0')
    ylabel('Firing rate (sp/s)');
    

![../../_images/1-intro-to-brian-neurons_image_52_0.png](../../_images/1-intro-to-brian-neurons_image_52_0.png)

The line `v0 : 1` declares a new per-neuron parameter `v0` with units `1` (i.e. dimensionless).

The line `G.v0 = 'i*v0_max/(N-1)'` initialises the value of v0 for each neuron varying from 0 up to `v0_max`. The symbol `i` when it appears in strings like this refers to the neuron index.

So in this example, we’re driving the neuron towards the value `v0` exponentially, but when `v` crosses `v>1`, it fires a spike and resets. The effect is that the rate at which it fires spikes will be related to the value of `v0`. For `v0<1` it will never fire a spike, and as `v0` gets larger it will fire spikes at a higher rate. The right hand plot shows the firing rate as a function of the value of `v0`. This is the I-f curve of this neuron model.

Note that in the plot we’ve used the `count` variable of the `SpikeMonitor`: this is an array of the number of spikes each neuron in the group fired. Dividing this by the duration of the run gives the firing rate.

## Stochastic neurons

Often when making models of neurons, we include a random element to model the effect of various forms of neural noise. In Brian, we can do this by using the symbol `xi` in differential equations. Strictly speaking, this symbol is a “stochastic differential” but you can sort of thinking of it as just a Gaussian random variable with mean 0 and standard deviation 1. We do have to take into account the way stochastic differentials scale with time, which is why we multiply it by `tau**-0.5` in the equations below (see a textbook on stochastic differential equations for more details). Note that we also changed the `method` keyword argument to use `'euler'` (which stands for the [Euler-Maruyama method](https://en.wikipedia.org/wiki/Euler%E2%80%93Maruyama_method)); the `'exact'` method that we used earlier is not applicable to stochastic differential equations.
    
    
    start_scope()
    
    N = 100
    tau = 10*ms
    v0_max = 3.
    duration = 1000*ms
    sigma = 0.2
    
    eqs = '''
    dv/dt = (v0-v)/tau+sigma*xi*tau**-0.5 : 1 (unless refractory)
    v0 : 1
    '''
    
    G = NeuronGroup(N, eqs, threshold='v>1', reset='v=0', refractory=5*ms, method='euler')
    M = SpikeMonitor(G)
    
    G.v0 = 'i*v0_max/(N-1)'
    
    run(duration)
    
    figure(figsize=(12,4))
    subplot(121)
    plot(M.t/ms, M.i, '.k')
    xlabel('Time (ms)')
    ylabel('Neuron index')
    subplot(122)
    plot(G.v0, M.count/duration)
    xlabel('v0')
    ylabel('Firing rate (sp/s)');
    

![../../_images/1-intro-to-brian-neurons_image_55_0.png](../../_images/1-intro-to-brian-neurons_image_55_0.png)

That’s the same figure as in the previous section but with some noise added. Note how the curve has changed shape: instead of a sharp jump from firing at rate 0 to firing at a positive rate, it now increases in a sigmoidal fashion. This is because no matter how small the driving force the randomness may cause it to fire a spike.

## End of tutorial

That’s the end of this part of the tutorial. The cell below has another example. See if you can work out what it is doing and why. Try adding a `StateMonitor` to record the values of the variables for one of the neurons to help you understand it.

You could also try out the things you’ve learned in this cell.

Once you’re done with that you can move on to the next tutorial on Synapses.
    
    
    start_scope()
    
    N = 1000
    tau = 10*ms
    vr = -70*mV
    vt0 = -50*mV
    delta_vt0 = 5*mV
    tau_t = 100*ms
    sigma = 0.5*(vt0-vr)
    v_drive = 2*(vt0-vr)
    duration = 100*ms
    
    eqs = '''
    dv/dt = (v_drive+vr-v)/tau + sigma*xi*tau**-0.5 : volt
    dvt/dt = (vt0-vt)/tau_t : volt
    '''
    
    reset = '''
    v = vr
    vt += delta_vt0
    '''
    
    G = NeuronGroup(N, eqs, threshold='v>vt', reset=reset, refractory=5*ms, method='euler')
    spikemon = SpikeMonitor(G)
    
    G.v = 'rand()*(vt0-vr)+vr'
    G.vt = vt0
    
    run(duration)
    
    _ = hist(spikemon.t/ms, 100, histtype='stepfilled', facecolor='k', weights=list(ones(len(spikemon))/(N*defaultclock.dt)))
    xlabel('Time (ms)')
    ylabel('Instantaneous firing rate (sp/s)');
    

![../../_images/1-intro-to-brian-neurons_image_58_0.png](../../_images/1-intro-to-brian-neurons_image_58_0.png)

---

# Introduction to Brian part 2: Synapses2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/resources/tutorials/2-intro-to-brian-synapses.html

# Introduction to Brian part 2: Synapses

Note

This tutorial is a static non-editable version. You can launch an interactive, editable version without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=tutorials/2-intro-to-brian-synapses.ipynb)

Alternatively, you can download a copy of the notebook file to use locally: [`2-intro-to-brian-synapses.ipynb`](../../_downloads/78f571f7cac5f8cd63a551b192d61edc/2-intro-to-brian-synapses.ipynb)

See the [tutorial overview page](index.html) for more details.

If you haven’t yet read part 1: Neurons, go read that now.

As before we start by importing the Brian package and setting up matplotlib for IPython:
    
    
    from brian2 import *
    %matplotlib inline
    

## The simplest Synapse

Once you have some neurons, the next step is to connect them up via synapses. We’ll start out with doing the simplest possible type of synapse that causes an instantaneous change in a variable after a spike.
    
    
    start_scope()
    
    eqs = '''
    dv/dt = (I-v)/tau : 1
    I : 1
    tau : second
    '''
    G = NeuronGroup(2, eqs, threshold='v>1', reset='v = 0', method='exact')
    G.I = [2, 0]
    G.tau = [10, 100]*ms
    
    # Comment these two lines out to see what happens without Synapses
    S = Synapses(G, G, on_pre='v_post += 0.2')
    S.connect(i=0, j=1)
    
    M = StateMonitor(G, 'v', record=True)
    
    run(100*ms)
    
    plot(M.t/ms, M.v[0], label='Neuron 0')
    plot(M.t/ms, M.v[1], label='Neuron 1')
    xlabel('Time (ms)')
    ylabel('v')
    legend();
    
    
    
    <matplotlib.legend.Legend at 0x7fdccb8773d0>
    

![../../_images/2-intro-to-brian-synapses_image_5_1.png](../../_images/2-intro-to-brian-synapses_image_5_1.png)

There are a few things going on here. First of all, let’s recap what is going on with the `NeuronGroup`. We’ve created two neurons, each of which has the same differential equation but different values for parameters I and tau. Neuron 0 has `I=2` and `tau=10*ms` which means that is driven to repeatedly spike at a fairly high rate. Neuron 1 has `I=0` and `tau=100*ms` which means that on its own - without the synapses - it won’t spike at all (the driving current I is 0). You can prove this to yourself by commenting out the two lines that define the synapse.

Next we define the synapses: `Synapses(source, target, ...)` means that we are defining a synaptic model that goes from `source` to `target`. In this case, the source and target are both the same, the group `G`. The syntax `on_pre='v_post += 0.2'` means that when a spike occurs in the presynaptic neuron (hence `on_pre`) it causes an instantaneous change to happen `v_post += 0.2`. The `_post` means that the value of `v` referred to is the post-synaptic value, and it is increased by 0.2. So in total, what this model says is that whenever two neurons in G are connected by a synapse, when the source neuron fires a spike the target neuron will have its value of `v` increased by 0.2.

However, at this point we have only defined the synapse model, we haven’t actually created any synapses. The next line `S.connect(i=0, j=1)` creates a synapse from neuron 0 to neuron 1.

## Adding a weight

In the previous section, we hard coded the weight of the synapse to be the value 0.2, but often we would to allow this to be different for different synapses. We do that by introducing synapse equations.
    
    
    start_scope()
    
    eqs = '''
    dv/dt = (I-v)/tau : 1
    I : 1
    tau : second
    '''
    G = NeuronGroup(3, eqs, threshold='v>1', reset='v = 0', method='exact')
    G.I = [2, 0, 0]
    G.tau = [10, 100, 100]*ms
    
    # Comment these two lines out to see what happens without Synapses
    S = Synapses(G, G, 'w : 1', on_pre='v_post += w')
    S.connect(i=0, j=[1, 2])
    S.w = 'j*0.2'
    
    M = StateMonitor(G, 'v', record=True)
    
    run(50*ms)
    
    plot(M.t/ms, M.v[0], label='Neuron 0')
    plot(M.t/ms, M.v[1], label='Neuron 1')
    plot(M.t/ms, M.v[2], label='Neuron 2')
    xlabel('Time (ms)')
    ylabel('v')
    legend();
    
    
    
    <matplotlib.legend.Legend at 0x7fdccb7f2750>
    

![../../_images/2-intro-to-brian-synapses_image_8_1.png](../../_images/2-intro-to-brian-synapses_image_8_1.png)

This example behaves very similarly to the previous example, but now there’s a synaptic weight variable `w`. The string `'w : 1'` is an equation string, precisely the same as for neurons, that defines a single dimensionless parameter `w`. We changed the behaviour on a spike to `on_pre='v_post += w'` now, so that each synapse can behave differently depending on the value of `w`. To illustrate this, we’ve made a third neuron which behaves precisely the same as the second neuron, and connected neuron 0 to both neurons 1 and 2. We’ve also set the weights via `S.w = 'j*0.2'`. When `i` and `j` occur in the context of synapses, `i` refers to the source neuron index, and `j` to the target neuron index. So this will give a synaptic connection from 0 to 1 with weight `0.2=0.2*1` and from 0 to 2 with weight `0.4=0.2*2`.

## Introducing a delay

So far, the synapses have been instantaneous, but we can also make them act with a certain delay.
    
    
    start_scope()
    
    eqs = '''
    dv/dt = (I-v)/tau : 1
    I : 1
    tau : second
    '''
    G = NeuronGroup(3, eqs, threshold='v>1', reset='v = 0', method='exact')
    G.I = [2, 0, 0]
    G.tau = [10, 100, 100]*ms
    
    S = Synapses(G, G, 'w : 1', on_pre='v_post += w')
    S.connect(i=0, j=[1, 2])
    S.w = 'j*0.2'
    S.delay = 'j*2*ms'
    
    M = StateMonitor(G, 'v', record=True)
    
    run(50*ms)
    
    plot(M.t/ms, M.v[0], label='Neuron 0')
    plot(M.t/ms, M.v[1], label='Neuron 1')
    plot(M.t/ms, M.v[2], label='Neuron 2')
    xlabel('Time (ms)')
    ylabel('v')
    legend();
    
    
    
    <matplotlib.legend.Legend at 0x7fdccb7f2290>
    

![../../_images/2-intro-to-brian-synapses_image_11_1.png](../../_images/2-intro-to-brian-synapses_image_11_1.png)

As you can see, that’s as simple as adding a line `S.delay = 'j*2*ms'` so that the synapse from 0 to 1 has a delay of 2 ms, and from 0 to 2 has a delay of 4 ms.

## More complex connectivity

So far, we specified the synaptic connectivity explicitly, but for larger networks this isn’t usually possible. For that, we usually want to specify some condition.
    
    
    start_scope()
    
    N = 10
    G = NeuronGroup(N, 'v:1')
    S = Synapses(G, G)
    S.connect(condition='i!=j', p=0.2)
    

Here we’ve created a dummy neuron group of N neurons and a dummy synapses model that doens’t actually do anything just to demonstrate the connectivity. The line `S.connect(condition='i!=j', p=0.2)` will connect all pairs of neurons `i` and `j` with probability 0.2 as long as the condition `i!=j` holds. So, how can we see that connectivity? Here’s a little function that will let us visualise it.
    
    
    def visualise_connectivity(S):
        Ns = len(S.source)
        Nt = len(S.target)
        figure(figsize=(10, 4))
        subplot(121)
        plot(zeros(Ns), arange(Ns), 'ok', ms=10)
        plot(ones(Nt), arange(Nt), 'ok', ms=10)
        for i, j in zip(S.i, S.j):
            plot([0, 1], [i, j], '-k')
        xticks([0, 1], ['Source', 'Target'])
        ylabel('Neuron index')
        xlim(-0.1, 1.1)
        ylim(-1, max(Ns, Nt))
        subplot(122)
        plot(S.i, S.j, 'ok')
        xlim(-1, Ns)
        ylim(-1, Nt)
        xlabel('Source neuron index')
        ylabel('Target neuron index')
    
    visualise_connectivity(S)
    

![../../_images/2-intro-to-brian-synapses_image_16_0.png](../../_images/2-intro-to-brian-synapses_image_16_0.png)

There are two plots here. On the left hand side, you see a vertical line of circles indicating source neurons on the left, and a vertical line indicating target neurons on the right, and a line between two neurons that have a synapse. On the right hand side is another way of visualising the same thing. Here each black dot is a synapse, with x value the source neuron index, and y value the target neuron index.

Let’s see how these figures change as we change the probability of a connection:
    
    
    start_scope()
    
    N = 10
    G = NeuronGroup(N, 'v:1')
    
    for p in [0.1, 0.5, 1.0]:
        S = Synapses(G, G)
        S.connect(condition='i!=j', p=p)
        visualise_connectivity(S)
        suptitle('p = '+str(p));
    

![../../_images/2-intro-to-brian-synapses_image_18_0.png](../../_images/2-intro-to-brian-synapses_image_18_0.png) ![../../_images/2-intro-to-brian-synapses_image_18_1.png](../../_images/2-intro-to-brian-synapses_image_18_1.png) ![../../_images/2-intro-to-brian-synapses_image_18_2.png](../../_images/2-intro-to-brian-synapses_image_18_2.png)

And let’s see what another connectivity condition looks like. This one will only connect neighbouring neurons.
    
    
    start_scope()
    
    N = 10
    G = NeuronGroup(N, 'v:1')
    
    S = Synapses(G, G)
    S.connect(condition='abs(i-j)<4 and i!=j')
    visualise_connectivity(S)
    

![../../_images/2-intro-to-brian-synapses_image_20_0.png](../../_images/2-intro-to-brian-synapses_image_20_0.png)

Try using that cell to see how other connectivity conditions look like.

You can also use the generator syntax to create connections like this more efficiently. In small examples like this, it doesn’t matter, but for large numbers of neurons it can be much more efficient to specify directly which neurons should be connected than to specify just a condition. Note that the following example uses `skip_if_invalid` to avoid errors at the boundaries (e.g. do not try to connect the neuron with index 1 to a neuron with index -2).
    
    
    start_scope()
    
    N = 10
    G = NeuronGroup(N, 'v:1')
    
    S = Synapses(G, G)
    S.connect(j='k for k in range(i-3, i+4) if i!=k', skip_if_invalid=True)
    visualise_connectivity(S)
    

![../../_images/2-intro-to-brian-synapses_image_23_0.png](../../_images/2-intro-to-brian-synapses_image_23_0.png)

If each source neuron is connected to precisely one target neuron (which would be normally used with two separate groups of the same size, not with identical source and target groups as in this example), there is a special syntax that is extremely efficient. For example, 1-to-1 connectivity looks like this:
    
    
    start_scope()
    
    N = 10
    G = NeuronGroup(N, 'v:1')
    
    S = Synapses(G, G)
    S.connect(j='i')
    visualise_connectivity(S)
    

![../../_images/2-intro-to-brian-synapses_image_25_0.png](../../_images/2-intro-to-brian-synapses_image_25_0.png)

You can also do things like specifying the value of weights with a string. Let’s see an example where we assign each neuron a spatial location and have a distance-dependent connectivity function. We visualise the weight of a synapse by the size of the marker.
    
    
    start_scope()
    
    N = 30
    neuron_spacing = 50*umetre
    width = N/4.0*neuron_spacing
    
    # Neuron has one variable x, its position
    G = NeuronGroup(N, 'x : metre')
    G.x = 'i*neuron_spacing'
    
    # All synapses are connected (excluding self-connections)
    S = Synapses(G, G, 'w : 1')
    S.connect(condition='i!=j')
    # Weight varies with distance
    S.w = 'exp(-(x_pre-x_post)**2/(2*width**2))'
    
    scatter(S.x_pre/um, S.x_post/um, S.w*20)
    xlabel('Source neuron position (um)')
    ylabel('Target neuron position (um)');
    
    
    
    Text(0, 0.5, 'Target neuron position (um)')
    

![../../_images/2-intro-to-brian-synapses_image_27_1.png](../../_images/2-intro-to-brian-synapses_image_27_1.png)

Now try changing that function and seeing how the plot changes.

## More complex synapse models: STDP

Brian’s synapse framework is very general and can do things like short-term plasticity (STP) or spike-timing dependent plasticity (STDP). Let’s see how that works for STDP.

STDP is normally defined by an equation something like this:

\\[\Delta w = \sum_{t_{pre}} \sum_{t_{post}} W(t_{post}-t_{pre})\\]

That is, the change in synaptic weight w is the sum over all presynaptic spike times \\(t_{pre}\\) and postsynaptic spike times \\(t_{post}\\) of some function \\(W\\) of the difference in these spike times. A commonly used function \\(W\\) is:

\\[\begin{split}W(\Delta t) = \begin{cases} A_{pre} e^{-\Delta t/\tau_{pre}} & \Delta t>0 \\\ A_{post} e^{\Delta t/\tau_{post}} & \Delta t<0 \end{cases}\end{split}\\]

This function looks like this:
    
    
    tau_pre = tau_post = 20*ms
    A_pre = 0.01
    A_post = -A_pre*1.05
    delta_t = linspace(-50, 50, 100)*ms
    W = where(delta_t>0, A_pre*exp(-delta_t/tau_pre), A_post*exp(delta_t/tau_post))
    plot(delta_t/ms, W)
    xlabel(r'$\Delta t$ (ms)')
    ylabel('W')
    axhline(0, ls='-', c='k');
    
    
    
    <matplotlib.lines.Line2D at 0x7fdccb5acdd0>
    

![../../_images/2-intro-to-brian-synapses_image_29_1.png](../../_images/2-intro-to-brian-synapses_image_29_1.png)

Simulating it directly using this equation though would be very inefficient, because we would have to sum over all pairs of spikes. That would also be physiologically unrealistic because the neuron cannot remember all its previous spike times. It turns out there is a more efficient and physiologically more plausible way to get the same effect.

We define two new variables \\(a_{pre}\\) and \\(a_{post}\\) which are “traces” of pre- and post-synaptic activity, governed by the differential equations:

\\[\begin{split}\begin{aligned} \tau_{pre}\frac{\mathrm{d}}{\mathrm{d}t} a_{pre} &= -a_{pre}\\\ \tau_{post}\frac{\mathrm{d}}{\mathrm{d}t} a_{post} &= -a_{post} \end{aligned}\end{split}\\]

When a presynaptic spike occurs, the presynaptic trace is updated and the weight is modified according to the rule:

\\[\begin{split}\begin{aligned} a_{pre} &\rightarrow a_{pre}+A_{pre}\\\ w &\rightarrow w+a_{post} \end{aligned}\end{split}\\]

When a postsynaptic spike occurs:

\\[\begin{split}\begin{aligned} a_{post} &\rightarrow a_{post}+A_{post}\\\ w &\rightarrow w+a_{pre} \end{aligned}\end{split}\\]

To see that this formulation is equivalent, you just have to check that the equations sum linearly, and consider two cases: what happens if the presynaptic spike occurs before the postsynaptic spike, and vice versa. Try drawing a picture of it.

Now that we have a formulation that relies only on differential equations and spike events, we can turn that into Brian code.
    
    
    start_scope()
    
    taupre = taupost = 20*ms
    wmax = 0.01
    Apre = 0.01
    Apost = -Apre*taupre/taupost*1.05
    
    G = NeuronGroup(1, 'v:1', threshold='v>1', reset='')
    
    S = Synapses(G, G,
                 '''
                 w : 1
                 dapre/dt = -apre/taupre : 1 (event-driven)
                 dapost/dt = -apost/taupost : 1 (event-driven)
                 ''',
                 on_pre='''
                 v_post += w
                 apre += Apre
                 w = clip(w+apost, 0, wmax)
                 ''',
                 on_post='''
                 apost += Apost
                 w = clip(w+apre, 0, wmax)
                 ''')
    

There are a few things to see there. Firstly, when defining the synapses we’ve given a more complicated multi-line string defining three synaptic variables (`w`, `apre` and `apost`). We’ve also got a new bit of syntax there, `(event-driven)` after the definitions of `apre` and `apost`. What this means is that although these two variables evolve continuously over time, Brian should only update them at the time of an event (a spike). This is because we don’t need the values of `apre` and `apost` except at spike times, and it is more efficient to only update them when needed.

Next we have a `on_pre=...` argument. The first line is `v_post += w`: this is the line that actually applies the synaptic weight to the target neuron. The second line is `apre += Apre` which encodes the rule above. In the third line, we’re also encoding the rule above but we’ve added one extra feature: we’ve clamped the synaptic weights between a minimum of 0 and a maximum of `wmax` so that the weights can’t get too large or negative. The function `clip(x, low, high)` does this.

Finally, we have a `on_post=...` argument. This gives the statements to calculate when a post-synaptic neuron fires. Note that we do not modify `v` in this case, only the synaptic variables.

Now let’s see how all the variables behave when a presynaptic spike arrives some time before a postsynaptic spike.
    
    
    start_scope()
    
    taupre = taupost = 20*ms
    wmax = 0.01
    Apre = 0.01
    Apost = -Apre*taupre/taupost*1.05
    
    G = NeuronGroup(2, 'v:1', threshold='t>(1+i)*10*ms', refractory=100*ms)
    
    S = Synapses(G, G,
                 '''
                 w : 1
                 dapre/dt = -apre/taupre : 1 (clock-driven)
                 dapost/dt = -apost/taupost : 1 (clock-driven)
                 ''',
                 on_pre='''
                 v_post += w
                 apre += Apre
                 w = clip(w+apost, 0, wmax)
                 ''',
                 on_post='''
                 apost += Apost
                 w = clip(w+apre, 0, wmax)
                 ''', method='linear')
    S.connect(i=0, j=1)
    M = StateMonitor(S, ['w', 'apre', 'apost'], record=True)
    
    run(30*ms)
    
    figure(figsize=(4, 8))
    subplot(211)
    plot(M.t/ms, M.apre[0], label='apre')
    plot(M.t/ms, M.apost[0], label='apost')
    legend()
    subplot(212)
    plot(M.t/ms, M.w[0], label='w')
    legend(loc='best')
    xlabel('Time (ms)');
    
    
    
    Text(0.5, 0, 'Time (ms)')
    

![../../_images/2-intro-to-brian-synapses_image_33_1.png](../../_images/2-intro-to-brian-synapses_image_33_1.png)

A couple of things to note here. First of all, we’ve used a trick to make neuron 0 fire a spike at time 10 ms, and neuron 1 at time 20 ms. Can you see how that works?

Secondly, we’ve replaced the `(event-driven)` by `(clock-driven)` so you can see how `apre` and `apost` evolve over time. Try reverting this change and see what happens.

Try changing the times of the spikes to see what happens.

Finally, let’s verify that this formulation is equivalent to the original one.
    
    
    start_scope()
    
    taupre = taupost = 20*ms
    Apre = 0.01
    Apost = -Apre*taupre/taupost*1.05
    tmax = 50*ms
    N = 100
    
    # Presynaptic neurons G spike at times from 0 to tmax
    # Postsynaptic neurons G spike at times from tmax to 0
    # So difference in spike times will vary from -tmax to +tmax
    G = NeuronGroup(N, 'tspike:second', threshold='t>tspike', refractory=100*ms)
    H = NeuronGroup(N, 'tspike:second', threshold='t>tspike', refractory=100*ms)
    G.tspike = 'i*tmax/(N-1)'
    H.tspike = '(N-1-i)*tmax/(N-1)'
    
    S = Synapses(G, H,
                 '''
                 w : 1
                 dapre/dt = -apre/taupre : 1 (event-driven)
                 dapost/dt = -apost/taupost : 1 (event-driven)
                 ''',
                 on_pre='''
                 apre += Apre
                 w = w+apost
                 ''',
                 on_post='''
                 apost += Apost
                 w = w+apre
                 ''')
    S.connect(j='i')
    
    run(tmax+1*ms)
    
    plot((H.tspike-G.tspike)/ms, S.w)
    xlabel(r'$\Delta t$ (ms)')
    ylabel(r'$\Delta w$')
    axhline(0, ls='-', c='k');
    
    
    
    <matplotlib.lines.Line2D at 0x7fdcc8ae8890>
    

![../../_images/2-intro-to-brian-synapses_image_35_1.png](../../_images/2-intro-to-brian-synapses_image_35_1.png)

Can you see how this works?

## End of tutorial

---

# Introduction to Brian part 3: Simulations2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/resources/tutorials/3-intro-to-brian-simulations.html

# Introduction to Brian part 3: Simulations

If you haven’t yet read parts 1 and 2 on Neurons and Synapses, go read them first.

This tutorial is about managing the slightly more complicated tasks that crop up in research problems, rather than the toy examples we’ve been looking at so far. So we cover things like inputting sensory data, modelling experimental conditions, etc.

As before we start by importing the Brian package and setting up matplotlib for IPython:

Note

This tutorial is a static non-editable version. You can launch an interactive, editable version without installing any local files using the Binder service (although note that at some times this may be slow or fail to open): [![launchbinder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/brian-team/brian2-binder/master?filepath=tutorials/3-intro-to-brian-simulations.ipynb)

Alternatively, you can download a copy of the notebook file to use locally: [`3-intro-to-brian-simulations.ipynb`](../../_downloads/af3f67f9fd5af3c6ed7e83eaaf0ab632/3-intro-to-brian-simulations.ipynb)

See the [tutorial overview page](index.html) for more details.
    
    
    from brian2 import *
    %matplotlib inline
    

## Multiple runs

Let’s start by looking at a very common task: doing multiple runs of a simulation with some parameter that changes. Let’s start off with something very simple, how does the firing rate of a leaky integrate-and-fire neuron driven by Poisson spiking neurons change depending on its membrane time constant? Let’s set that up.
    
    
    # remember, this is here for running separate simulations in the same notebook
    start_scope()
    # Parameters
    num_inputs = 100
    input_rate = 10*Hz
    weight = 0.1
    # Range of time constants
    tau_range = linspace(1, 10, 30)*ms
    # Use this list to store output rates
    output_rates = []
    # Iterate over range of time constants
    for tau in tau_range:
        # Construct the network each time
        P = PoissonGroup(num_inputs, rates=input_rate)
        eqs = '''
        dv/dt = -v/tau : 1
        '''
        G = NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='exact')
        S = Synapses(P, G, on_pre='v += weight')
        S.connect()
        M = SpikeMonitor(G)
        # Run it and store the output firing rate in the list
        run(1*second)
        output_rates.append(M.num_spikes/second)
    # And plot it
    plot(tau_range/ms, output_rates)
    xlabel(r'$\tau$ (ms)')
    ylabel('Firing rate (sp/s)');
    

![../../_images/3-intro-to-brian-simulations_image_4_0.png](../../_images/3-intro-to-brian-simulations_image_4_0.png)

Now if you’re running the notebook, you’ll see that this was a little slow to run. The reason is that for each loop, you’re recreating the objects from scratch. We can improve that by setting up the network just once. We store a copy of the state of the network before the loop, and restore it at the beginning of each iteration.
    
    
    start_scope()
    num_inputs = 100
    input_rate = 10*Hz
    weight = 0.1
    tau_range = linspace(1, 10, 30)*ms
    output_rates = []
    # Construct the network just once
    P = PoissonGroup(num_inputs, rates=input_rate)
    eqs = '''
    dv/dt = -v/tau : 1
    '''
    G = NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='exact')
    S = Synapses(P, G, on_pre='v += weight')
    S.connect()
    M = SpikeMonitor(G)
    # Store the current state of the network
    store()
    for tau in tau_range:
        # Restore the original state of the network
        restore()
        # Run it with the new value of tau
        run(1*second)
        output_rates.append(M.num_spikes/second)
    plot(tau_range/ms, output_rates)
    xlabel(r'$\tau$ (ms)')
    ylabel('Firing rate (sp/s)');
    

![../../_images/3-intro-to-brian-simulations_image_6_0.png](../../_images/3-intro-to-brian-simulations_image_6_0.png)

That’s a very simple example of using store and restore, but you can use it in much more complicated situations. For example, you might want to run a long training run, and then run multiple test runs afterwards. Simply put a store after the long training run, and a restore before each testing run.

You can also see that the output curve is very noisy and doesn’t increase monotonically like we’d expect. The noise is coming from the fact that we run the Poisson group afresh each time. If we only wanted to see the effect of the time constant, we could make sure that the spikes were the same each time (although note that really, you ought to do multiple runs and take an average). We do this by running just the Poisson group once, recording its spikes, and then creating a new `SpikeGeneratorGroup` that will output those recorded spikes each time.
    
    
    start_scope()
    num_inputs = 100
    input_rate = 10*Hz
    weight = 0.1
    tau_range = linspace(1, 10, 30)*ms
    output_rates = []
    # Construct the Poisson spikes just once
    P = PoissonGroup(num_inputs, rates=input_rate)
    MP = SpikeMonitor(P)
    # We use a Network object because later on we don't
    # want to include these objects
    net = Network(P, MP)
    net.run(1*second)
    # And keep a copy of those spikes
    spikes_i = MP.i
    spikes_t = MP.t
    # Now construct the network that we run each time
    # SpikeGeneratorGroup gets the spikes that we created before
    SGG = SpikeGeneratorGroup(num_inputs, spikes_i, spikes_t)
    eqs = '''
    dv/dt = -v/tau : 1
    '''
    G = NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='exact')
    S = Synapses(SGG, G, on_pre='v += weight')
    S.connect()
    M = SpikeMonitor(G)
    # Store the current state of the network
    net = Network(SGG, G, S, M)
    net.store()
    for tau in tau_range:
        # Restore the original state of the network
        net.restore()
        # Run it with the new value of tau
        net.run(1*second)
        output_rates.append(M.num_spikes/second)
    plot(tau_range/ms, output_rates)
    xlabel(r'$\tau$ (ms)')
    ylabel('Firing rate (sp/s)');
    

![../../_images/3-intro-to-brian-simulations_image_8_0.png](../../_images/3-intro-to-brian-simulations_image_8_0.png)

You can see that now there is much less noise and it increases monotonically because the input spikes are the same each time, meaning we’re seeing the effect of the time constant, not the random spikes.

Note that in the code above, we created `Network` objects. The reason is that in the loop, if we just called `run` it would try to simulate all the objects, including the Poisson neurons `P`, and we only want to run that once. We use `Network` to specify explicitly which objects we want to include.

The techniques we’ve looked at so far are the conceptually most simple way to do multiple runs, but not always the most efficient. Since there’s only a single output neuron in the model above, we can simply duplicate that output neuron and make the time constant a parameter of the group.
    
    
    start_scope()
    num_inputs = 100
    input_rate = 10*Hz
    weight = 0.1
    tau_range = linspace(1, 10, 30)*ms
    num_tau = len(tau_range)
    P = PoissonGroup(num_inputs, rates=input_rate)
    # We make tau a parameter of the group
    eqs = '''
    dv/dt = -v/tau : 1
    tau : second
    '''
    # And we have num_tau output neurons, each with a different tau
    G = NeuronGroup(num_tau, eqs, threshold='v>1', reset='v=0', method='exact')
    G.tau = tau_range
    S = Synapses(P, G, on_pre='v += weight')
    S.connect()
    M = SpikeMonitor(G)
    # Now we can just run once with no loop
    run(1*second)
    output_rates = M.count/second # firing rate is count/duration
    plot(tau_range/ms, output_rates)
    xlabel(r'$\tau$ (ms)')
    ylabel('Firing rate (sp/s)');
    
    
    
    WARNING    "tau" is an internal variable of group "neurongroup", but also exists in the run namespace with the value 10. * msecond. The internal variable will be used. [brian2.groups.group.Group.resolve.resolution_conflict]
    

![../../_images/3-intro-to-brian-simulations_image_10_1.png](../../_images/3-intro-to-brian-simulations_image_10_1.png)

You can see that this is much faster again! It’s a little bit more complicated conceptually, and it’s not always possible to do this trick, but it can be much more efficient if it’s possible.

Let’s finish with this example by having a quick look at how the mean and standard deviation of the interspike intervals depends on the time constant.
    
    
    trains = M.spike_trains()
    isi_mu = full(num_tau, nan)*second
    isi_std = full(num_tau, nan)*second
    for idx in range(num_tau):
        train = diff(trains[idx])
        if len(train)>1:
            isi_mu[idx] = mean(train)
            isi_std[idx] = std(train)
    errorbar(tau_range/ms, isi_mu/ms, yerr=isi_std/ms)
    xlabel(r'$\tau$ (ms)')
    ylabel('Interspike interval (ms)');
    

![../../_images/3-intro-to-brian-simulations_image_12_0.png](../../_images/3-intro-to-brian-simulations_image_12_0.png)

Notice that we used the `spike_trains()` method of `SpikeMonitor`. This is a dictionary with keys being the indices of the neurons and values being the array of spike times for that neuron.

## Changing things during a run

Imagine an experiment where you inject current into a neuron, and change the amplitude randomly every 10 ms. Let’s see if we can model that using a Hodgkin-Huxley type neuron.
    
    
    start_scope()
    # Parameters
    area = 20000*umetre**2
    Cm = 1*ufarad*cm**-2 * area
    gl = 5e-5*siemens*cm**-2 * area
    El = -65*mV
    EK = -90*mV
    ENa = 50*mV
    g_na = 100*msiemens*cm**-2 * area
    g_kd = 30*msiemens*cm**-2 * area
    VT = -63*mV
    # The model
    eqs_HH = '''
    dv/dt = (gl*(El-v) - g_na*(m*m*m)*h*(v-ENa) - g_kd*(n*n*n*n)*(v-EK) + I)/Cm : volt
    dm/dt = 0.32*(mV**-1)*(13.*mV-v+VT)/
        (exp((13.*mV-v+VT)/(4.*mV))-1.)/ms*(1-m)-0.28*(mV**-1)*(v-VT-40.*mV)/
        (exp((v-VT-40.*mV)/(5.*mV))-1.)/ms*m : 1
    dn/dt = 0.032*(mV**-1)*(15.*mV-v+VT)/
        (exp((15.*mV-v+VT)/(5.*mV))-1.)/ms*(1.-n)-.5*exp((10.*mV-v+VT)/(40.*mV))/ms*n : 1
    dh/dt = 0.128*exp((17.*mV-v+VT)/(18.*mV))/ms*(1.-h)-4./(1+exp((40.*mV-v+VT)/(5.*mV)))/ms*h : 1
    I : amp
    '''
    group = NeuronGroup(1, eqs_HH,
                        threshold='v > -40*mV',
                        refractory='v > -40*mV',
                        method='exponential_euler')
    group.v = El
    statemon = StateMonitor(group, 'v', record=True)
    spikemon = SpikeMonitor(group, variables='v')
    figure(figsize=(9, 4))
    for l in range(5):
        group.I = rand()*50*nA
        run(10*ms)
        axvline(l*10, ls='--', c='k')
    axhline(El/mV, ls='-', c='lightgray', lw=3)
    plot(statemon.t/ms, statemon.v[0]/mV, '-b')
    plot(spikemon.t/ms, spikemon.v/mV, 'ob')
    xlabel('Time (ms)')
    ylabel('v (mV)');
    

![../../_images/3-intro-to-brian-simulations_image_14_0.png](../../_images/3-intro-to-brian-simulations_image_14_0.png)

In the code above, we used a loop over multiple runs to achieve this. That’s fine, but it’s not the most efficient way to do it because each time we call `run` we have to do a lot of initialisation work that slows everything down. It also won’t work as well with the more efficient standalone mode of Brian. Here’s another way.
    
    
    start_scope()
    group = NeuronGroup(1, eqs_HH,
                        threshold='v > -40*mV',
                        refractory='v > -40*mV',
                        method='exponential_euler')
    group.v = El
    statemon = StateMonitor(group, 'v', record=True)
    spikemon = SpikeMonitor(group, variables='v')
    # we replace the loop with a run_regularly
    group.run_regularly('I = rand()*50*nA', dt=10*ms)
    run(50*ms)
    figure(figsize=(9, 4))
    # we keep the loop just to draw the vertical lines
    for l in range(5):
        axvline(l*10, ls='--', c='k')
    axhline(El/mV, ls='-', c='lightgray', lw=3)
    plot(statemon.t/ms, statemon.v[0]/mV, '-b')
    plot(spikemon.t/ms, spikemon.v/mV, 'ob')
    xlabel('Time (ms)')
    ylabel('v (mV)');
    

![../../_images/3-intro-to-brian-simulations_image_16_0.png](../../_images/3-intro-to-brian-simulations_image_16_0.png)

We’ve replaced the loop that had multiple `run` calls with a `run_regularly`. This makes the specified block of code run every `dt=10*ms`. The `run_regularly` lets you run code specific to a single `NeuronGroup`, but sometimes you might need more flexibility. For this, you can use `network_operation` which lets you run arbitrary Python code (but won’t work with the standalone mode).
    
    
    start_scope()
    group = NeuronGroup(1, eqs_HH,
                        threshold='v > -40*mV',
                        refractory='v > -40*mV',
                        method='exponential_euler')
    group.v = El
    statemon = StateMonitor(group, 'v', record=True)
    spikemon = SpikeMonitor(group, variables='v')
    # we replace the loop with a network_operation
    @network_operation(dt=10*ms)
    def change_I():
        group.I = rand()*50*nA
    run(50*ms)
    figure(figsize=(9, 4))
    for l in range(5):
        axvline(l*10, ls='--', c='k')
    axhline(El/mV, ls='-', c='lightgray', lw=3)
    plot(statemon.t/ms, statemon.v[0]/mV, '-b')
    plot(spikemon.t/ms, spikemon.v/mV, 'ob')
    xlabel('Time (ms)')
    ylabel('v (mV)');
    

![../../_images/3-intro-to-brian-simulations_image_18_0.png](../../_images/3-intro-to-brian-simulations_image_18_0.png)

Now let’s extend this example to run on multiple neurons, each with a different capacitance to see how that affects the behaviour of the cell.
    
    
    start_scope()
    N = 3
    eqs_HH_2 = '''
    dv/dt = (gl*(El-v) - g_na*(m*m*m)*h*(v-ENa) - g_kd*(n*n*n*n)*(v-EK) + I)/C : volt
    dm/dt = 0.32*(mV**-1)*(13.*mV-v+VT)/
        (exp((13.*mV-v+VT)/(4.*mV))-1.)/ms*(1-m)-0.28*(mV**-1)*(v-VT-40.*mV)/
        (exp((v-VT-40.*mV)/(5.*mV))-1.)/ms*m : 1
    dn/dt = 0.032*(mV**-1)*(15.*mV-v+VT)/
        (exp((15.*mV-v+VT)/(5.*mV))-1.)/ms*(1.-n)-.5*exp((10.*mV-v+VT)/(40.*mV))/ms*n : 1
    dh/dt = 0.128*exp((17.*mV-v+VT)/(18.*mV))/ms*(1.-h)-4./(1+exp((40.*mV-v+VT)/(5.*mV)))/ms*h : 1
    I : amp
    C : farad
    '''
    group = NeuronGroup(N, eqs_HH_2,
                        threshold='v > -40*mV',
                        refractory='v > -40*mV',
                        method='exponential_euler')
    group.v = El
    # initialise with some different capacitances
    group.C = array([0.8, 1, 1.2])*ufarad*cm**-2*area
    statemon = StateMonitor(group, variables=True, record=True)
    # we go back to run_regularly
    group.run_regularly('I = rand()*50*nA', dt=10*ms)
    run(50*ms)
    figure(figsize=(9, 4))
    for l in range(5):
        axvline(l*10, ls='--', c='k')
    axhline(El/mV, ls='-', c='lightgray', lw=3)
    plot(statemon.t/ms, statemon.v.T/mV, '-')
    xlabel('Time (ms)')
    ylabel('v (mV)');
    

![../../_images/3-intro-to-brian-simulations_image_20_0.png](../../_images/3-intro-to-brian-simulations_image_20_0.png)

So that runs, but something looks wrong! The injected currents look like they’re different for all the different neurons! Let’s check:
    
    
    plot(statemon.t/ms, statemon.I.T/nA, '-')
    xlabel('Time (ms)')
    ylabel('I (nA)');
    

![../../_images/3-intro-to-brian-simulations_image_22_0.png](../../_images/3-intro-to-brian-simulations_image_22_0.png)

Sure enough, it’s different each time. But why? We wrote `group.run_regularly('I = rand()*50*nA', dt=10*ms)` which seems like it should give the same value of I for each neuron. But, like threshold and reset statements, `run_regularly` code is interpreted as being run separately for each neuron, and because I is a parameter, it can be different for each neuron. We can fix this by making I into a _shared_ variable, meaning it has the same value for each neuron.
    
    
    start_scope()
    N = 3
    eqs_HH_3 = '''
    dv/dt = (gl*(El-v) - g_na*(m*m*m)*h*(v-ENa) - g_kd*(n*n*n*n)*(v-EK) + I)/C : volt
    dm/dt = 0.32*(mV**-1)*(13.*mV-v+VT)/
        (exp((13.*mV-v+VT)/(4.*mV))-1.)/ms*(1-m)-0.28*(mV**-1)*(v-VT-40.*mV)/
        (exp((v-VT-40.*mV)/(5.*mV))-1.)/ms*m : 1
    dn/dt = 0.032*(mV**-1)*(15.*mV-v+VT)/
        (exp((15.*mV-v+VT)/(5.*mV))-1.)/ms*(1.-n)-.5*exp((10.*mV-v+VT)/(40.*mV))/ms*n : 1
    dh/dt = 0.128*exp((17.*mV-v+VT)/(18.*mV))/ms*(1.-h)-4./(1+exp((40.*mV-v+VT)/(5.*mV)))/ms*h : 1
    I : amp (shared) # everything is the same except we've added this shared
    C : farad
    '''
    group = NeuronGroup(N, eqs_HH_3,
                        threshold='v > -40*mV',
                        refractory='v > -40*mV',
                        method='exponential_euler')
    group.v = El
    group.C = array([0.8, 1, 1.2])*ufarad*cm**-2*area
    statemon = StateMonitor(group, 'v', record=True)
    group.run_regularly('I = rand()*50*nA', dt=10*ms)
    run(50*ms)
    figure(figsize=(9, 4))
    for l in range(5):
        axvline(l*10, ls='--', c='k')
    axhline(El/mV, ls='-', c='lightgray', lw=3)
    plot(statemon.t/ms, statemon.v.T/mV, '-')
    xlabel('Time (ms)')
    ylabel('v (mV)');
    

![../../_images/3-intro-to-brian-simulations_image_24_0.png](../../_images/3-intro-to-brian-simulations_image_24_0.png)

Ahh, that’s more like it!

## Adding input

Now let’s think about a neuron being driven by a sinusoidal input. Let’s go back to a leaky integrate-and-fire to simplify the equations a bit.
    
    
    start_scope()
    A = 2.5
    f = 10*Hz
    tau = 5*ms
    eqs = '''
    dv/dt = (I-v)/tau : 1
    I = A*sin(2*pi*f*t) : 1
    '''
    G = NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='euler')
    M = StateMonitor(G, variables=True, record=True)
    run(200*ms)
    plot(M.t/ms, M.v[0], label='v')
    plot(M.t/ms, M.I[0], label='I')
    xlabel('Time (ms)')
    ylabel('v')
    legend(loc='best');
    

![../../_images/3-intro-to-brian-simulations_image_26_0.png](../../_images/3-intro-to-brian-simulations_image_26_0.png)

So far, so good and the sort of thing we saw in the first tutorial. Now, what if that input current were something we had recorded and saved in a file? In that case, we can use `TimedArray`. Let’s start by reproducing the picture above but using `TimedArray`.
    
    
    start_scope()
    A = 2.5
    f = 10*Hz
    tau = 5*ms
    # Create a TimedArray and set the equations to use it
    t_recorded = arange(int(200*ms/defaultclock.dt))*defaultclock.dt
    I_recorded = TimedArray(A*sin(2*pi*f*t_recorded), dt=defaultclock.dt)
    eqs = '''
    dv/dt = (I-v)/tau : 1
    I = I_recorded(t) : 1
    '''
    G = NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='exact')
    M = StateMonitor(G, variables=True, record=True)
    run(200*ms)
    plot(M.t/ms, M.v[0], label='v')
    plot(M.t/ms, M.I[0], label='I')
    xlabel('Time (ms)')
    ylabel('v')
    legend(loc='best');
    

![../../_images/3-intro-to-brian-simulations_image_28_0.png](../../_images/3-intro-to-brian-simulations_image_28_0.png)

Note that for the example where we put the `sin` function directly in the equations, we had to use the `method='euler'` argument because the exact integrator wouldn’t work here (try it!). However, `TimedArray` is considered to be constant over its time step and so the linear integrator can be used. This means you won’t get the same behaviour from these two methods for two reasons. Firstly, the numerical integration methods `exact` and `euler` give slightly different results. Secondly, `sin` is not constant over a timestep whereas `TimedArray` is.

Now just to show that `TimedArray` works for arbitrary currents, let’s make a weird “recorded” current and run it on that.
    
    
    start_scope()
    A = 2.5
    f = 10*Hz
    tau = 5*ms
    # Let's create an array that couldn't be
    # reproduced with a formula
    num_samples = int(200*ms/defaultclock.dt)
    I_arr = zeros(num_samples)
    for _ in range(100):
        a = randint(num_samples)
        I_arr[a:a+100] = rand()
    I_recorded = TimedArray(A*I_arr, dt=defaultclock.dt)
    eqs = '''
    dv/dt = (I-v)/tau : 1
    I = I_recorded(t) : 1
    '''
    G = NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='exact')
    M = StateMonitor(G, variables=True, record=True)
    run(200*ms)
    plot(M.t/ms, M.v[0], label='v')
    plot(M.t/ms, M.I[0], label='I')
    xlabel('Time (ms)')
    ylabel('v')
    legend(loc='best');
    

![../../_images/3-intro-to-brian-simulations_image_30_0.png](../../_images/3-intro-to-brian-simulations_image_30_0.png)

Finally, let’s finish on an example that actually reads in some data from a file. See if you can work out how this example works.
    
    
    start_scope()
    from matplotlib.image import imread
    img = (1-imread('brian.png'))[::-1, :, 0].T
    num_samples, N = img.shape
    ta = TimedArray(img, dt=1*ms) # 228
    A = 1.5
    tau = 2*ms
    eqs = '''
    dv/dt = (A*ta(t, i)-v)/tau+0.8*xi*tau**-0.5 : 1
    '''
    G = NeuronGroup(N, eqs, threshold='v>1', reset='v=0', method='euler')
    M = SpikeMonitor(G)
    run(num_samples*ms)
    plot(M.t/ms, M.i, '.k', ms=3)
    xlim(0, num_samples)
    ylim(0, N)
    xlabel('Time (ms)')
    ylabel('Neuron index');
    

![../../_images/3-intro-to-brian-simulations_image_32_0.png](../../_images/3-intro-to-brian-simulations_image_32_0.png)

---

# Logging2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/advanced/logging.html

# Logging

Brian uses a logging system to display warnings and general information messages to the user, as well as writing them to a file with more detailed information, useful for debugging. Each log message has one of the following “log levels”:

`ERROR`
    

Only used when an exception is raised, i.e. an error occurs and the current operation is interrupted. _Example:_ You use a variable name in an equation that Brian does not recognize.

`WARNING`
    

Brian thinks that something is most likely a bug, but it cannot be sure. _Example:_ You use a [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses") object without any synapses in your simulation.

`INFO`
    

Brian wants to make the user aware of some automatic choice that it did for the user. _Example:_ You did not specify an integration `method` for a [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") and therefore Brian chose an appropriate method for you.

`DEBUG`
    

Additional information that might be useful when a simulation is not working as expected. _Example:_ The integration timestep used during the simulation.

`DIAGNOSTIC`
    

Additional information useful when tracking down bugs in Brian itself. _Example:_ The generated code for a `CodeObject`.

By default, all messages with level `DEBUG` or above are written to the log file and all messages of level `INFO` and above are displayed on the console. To change what messages are displayed, see below.

Note

By default, the log file is deleted after a successful simulation run, i.e. when the simulation exited without an error. To keep the log around, set the [logging.delete_log_on_exit](../reference/brian2.utils.html#brian-pref-logging-delete-log-on-exit) preference to `False`.

## Logging and multiprocessing

Brian’s logging system is not designed for multiple parallel Brian processes started via Python’s [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing "\(in Python v3.12\)") module (see the [multiprocessing examples](../examples/index.html#multiprocessing)). Log messages that get printed from different processes to the console are not printed in a well-defined order and do not contain any indication about which processes they are coming from. You might therefore consider using e.g. [`BrianLogger.log_level_error`](../reference/brian2.utils.logger.BrianLogger.html#brian2.utils.logger.BrianLogger.log_level_error "brian2.utils.logger.BrianLogger.log_level_error") to only show error messages before starting the processes and avoid cluttering your console with warning and info messages.

To avoid issues when multiple processes try to log to the same log file, file logging is automatically switched off for all processes except for the initial process. If you need a file log for sub-processes, you can call [`BrianLogger.initialize`](../reference/brian2.utils.logger.BrianLogger.html#brian2.utils.logger.BrianLogger.initialize "brian2.utils.logger.BrianLogger.initialize") in each sub-process. This way, each process will log to its own file.

## Showing/hiding log messages

If you want to change what messages are displayed on the console, you can call a method of the method of [`BrianLogger`](../reference/brian2.utils.logger.BrianLogger.html#brian2.utils.logger.BrianLogger "brian2.utils.logger.BrianLogger"):
    
    
    BrianLogger.log_level_debug() # now also display debug messages
    

It is also possible to suppress messages for certain sub-hierarchies by using [`BrianLogger.suppress_hierarchy`](../reference/brian2.utils.logger.BrianLogger.html#brian2.utils.logger.BrianLogger.suppress_hierarchy "brian2.utils.logger.BrianLogger.suppress_hierarchy"):
    
    
    # Suppress code generation messages on the console
    BrianLogger.suppress_hierarchy('brian2.codegen')
    # Suppress preference messages even in the log file
    BrianLogger.suppress_hierarchy('brian2.core.preferences',
                                   filter_log_file=True)
    

Similarly, messages ending in a certain name can be suppressed with [`BrianLogger.suppress_name`](../reference/brian2.utils.logger.BrianLogger.html#brian2.utils.logger.BrianLogger.suppress_name "brian2.utils.logger.BrianLogger.suppress_name"):
    
    
    # Suppress resolution conflict warnings
    BrianLogger.suppress_name('resolution_conflict')
    

These functions should be used with care, as they suppresses messages independent of the level, i.e. even warning and error messages.

## Preferences

You can also change details of the logging system via Brian’s [Preferences](preferences.html) system. With this mechanism, you can switch the logging to a file off completely (by setting [logging.file_log](../reference/brian2.utils.html#brian-pref-logging-file-log) to `False`) or have it log less messages (by setting [logging.file_log_level](../reference/brian2.utils.html#brian-pref-logging-file-log-level) to a level higher than `DEBUG`). To debug details of the code generation system, you can also set [logging.file_log_level](../reference/brian2.utils.html#brian-pref-logging-file-log-level) to `DIAGNOSTIC`. Note that this will make the log file grow quickly in size. To prevent it from filling up the disk, it will only be allowed to grow up to a certain size. You can configure the maximum file size with the [logging.file_log_max_size](../reference/brian2.utils.html#brian-pref-logging-file-log-max-size) preference.

For a list of all preferences related to logging, see the documentation of the [`brian2.utils.logger`](../reference/brian2.utils.html#module-brian2.utils.logger "brian2.utils.logger") module.

Warning

Most of the logging preferences are only taken into account during the initialization of the logging system which takes place as soon as `brian2` is imported. Therefore, if you use e.g. `prefs.logging.file_log = False` in your script, this will not have the intended effect! To make sure these preferences are taken into account, call [`BrianLogger.initialize`](../reference/brian2.utils.logger.BrianLogger.html#brian2.utils.logger.BrianLogger.initialize "brian2.utils.logger.BrianLogger.initialize") after setting the preferences. Alternatively, you can set the preferences in a file (see [Preferences](preferences.html)).

---

# Models and neuron groups2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/user/models.html

# Models and neuron groups

For Brian 1 users

See the document [Neural models (Brian 1 –> 2 conversion)](../introduction/brian1_to_2/neurongroup.html) for details how to convert Brian 1 code.

  * Model equations

  * Noise

  * Threshold and reset

  * Refractoriness

  * State variables

  * Subgroups

  * Shared variables

  * Storing state variables

  * Linked variables

  * Time scaling of noise

## Model equations

The core of every simulation is a [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup"), a group of neurons that share the same equations defining their properties. The minimum [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") specification contains the number of neurons and the model description in the form of equations:
    
    
    G = NeuronGroup(10, 'dv/dt = -v/(10*ms) : volt')
    

This defines a group of 10 leaky integrators. The model description can be directly given as a (possibly multi-line) string as above, or as an [`Equations`](../reference/brian2.equations.equations.Equations.html#brian2.equations.equations.Equations "brian2.equations.equations.Equations") object. For more details on the form of equations, see [Equations](equations.html). Brian needs the model to be given in the form of differential equations, but you might see the integrated form of synapses in some textbooks and papers. See [Converting from integrated form to ODEs](converting_from_integrated_form.html) for details on how to convert between these representations.

Note that model descriptions can make reference to physical units, but also to scalar variables declared outside of the model description itself:
    
    
    tau = 10*ms
    G = NeuronGroup(10, 'dv/dt = -v/tau : volt')
    

If a variable should be taken as a _parameter_ of the neurons, i.e. if it should be possible to vary its value across neurons, it has to be declared as part of the model description:
    
    
    G = NeuronGroup(10, '''dv/dt = -v/tau : volt
                           tau : second''')
    

To make complex model descriptions more readable, named subexpressions can be used:
    
    
    G = NeuronGroup(10, '''dv/dt = I_leak / Cm : volt
                           I_leak = g_L*(E_L - v) : amp''')
    

For a list of some standard model equations, see [Neural models (Brian 1 –> 2 conversion)](../introduction/brian1_to_2/neurongroup.html).

## Noise

In addition to ordinary differential equations, Brian allows you to introduce random noise by specifying a [stochastic differential equation](https://en.wikipedia.org/wiki/Stochastic_differential_equation). Brian uses the physicists’ notation used in the [Langevin equation](https://en.wikipedia.org/wiki/Langevin_equation), representing the “noise” as a term \\(\xi(t)\\), rather than the mathematicians’ stochastic differential \\(\mathrm{d}W_t\\). The following is an example of the [Ornstein-Uhlenbeck process](http://www.scholarpedia.org/article/Stochastic_dynamical_systems#Ornstein-Uhlenbeck_process) that is often used to model a leaky integrate-and-fire neuron with a stochastic current:
    
    
    G = NeuronGroup(10, 'dv/dt = -v/tau + sigma*sqrt(2/tau)*xi : volt')
    

You can start by thinking of `xi` as just a Gaussian random variable with mean 0 and standard deviation 1. However, it scales in an unusual way with time and this gives it units of `1/sqrt(second)`. You don’t necessarily need to understand why this is, but it is possible to get a reasonably simple intuition for it by thinking about numerical integration: see below.

Note

If you want to use noise in more than one equation of a [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") or [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses"), you will have to use suffixed names (see [Equation strings](equations.html#equation-strings) for details).

## Threshold and reset

To emit spikes, neurons need a _threshold_. Threshold and reset are given as strings in the [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") constructor:
    
    
    tau = 10*ms
    G = NeuronGroup(10, 'dv/dt = -v/tau : volt', threshold='v > -50*mV',
                    reset='v = -70*mV')
    

Whenever the threshold condition is fulfilled, the reset statements will be executed. Again, both threshold and reset can refer to physical units, external variables and parameters, in the same way as model descriptions:
    
    
    v_r = -70*mV  # reset potential
    G = NeuronGroup(10, '''dv/dt = -v/tau : volt
                           v_th : volt  # neuron-specific threshold''',
                    threshold='v > v_th', reset='v = v_r')
    

You can also create non-spike events. See [Custom events](../advanced/custom_events.html) for more details.

## Refractoriness

To make a neuron non-excitable for a certain time period after a spike, the refractory keyword can be used:
    
    
    G = NeuronGroup(10, 'dv/dt = -v/tau : volt', threshold='v > -50*mV',
                    reset='v = -70*mV', refractory=5*ms)
    

This will not allow any threshold crossing for a neuron for 5ms after a spike. The refractory keyword allows for more flexible refractoriness specifications, see [Refractoriness](refractoriness.html) for details.

## State variables

Differential equations and parameters in model descriptions are stored as _state variables_ of the [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup"). In addition to these variables, Brian also defines two variables automatically:

`i`
    

The index of a neuron.

`N`
    

The total number of neurons.

All state variables can be accessed and set as an attribute of the group. To get the values without physical units (e.g. for analysing data with external tools), use an underscore after the name:
    
    
    >>> G = NeuronGroup(10, '''dv/dt = -v/tau : volt
    ...                        tau : second''', name='neurons')
    >>> G.v = -70*mV
    >>> G.v
    <neurons.v: array([-70., -70., -70., -70., -70., -70., -70., -70., -70., -70.]) * mvolt>
    >>> G.v_  # values without units
    <neurons.v_: array([-0.07, -0.07, -0.07, -0.07, -0.07, -0.07, -0.07, -0.07, -0.07, -0.07])>
    

The value of state variables can also be set using string expressions that can refer to units and external variables, other state variables or mathematical functions:
    
    
    >>> G.tau = '5*ms + (1.0*i/N)*5*ms'
    >>> G.tau
    <neurons.tau: array([ 5. ,  5.5,  6. ,  6.5,  7. ,  7.5,  8. ,  8.5,  9. ,  9.5]) * msecond>
    

You can also set the value only if a condition holds, for example:
    
    
    >>> G.v['tau>7.25*ms'] = -60*mV
    >>> G.v
    <neurons.v: array([-70., -70., -70., -70., -70., -60., -60., -60., -60., -60.]) * mvolt>
    

## Subgroups

It is often useful to refer to a subset of neurons, this can be achieved using Python’s slicing syntax:
    
    
    G = NeuronGroup(10, '''dv/dt = -v/tau : volt
                           tau : second''',
                    threshold='v > -50*mV',
                    reset='v = -70*mV')
    # Create subgroups
    G1 = G[:5]
    G2 = G[5:]
    
    # This will set the values in the main group, subgroups are just "views"
    G1.tau = 10*ms
    G2.tau = 20*ms
    

Here `G1` refers to the first 5 neurons in G, and `G2` to the second 5 neurons. In general `G[i:j]` refers to the neurons with indices from `i` to `j-1`, as in general in Python.

For convenience, you can also use a single index, i.e. `G[i]` is equivalent to `G[i:i+1]`. In some situations, it can be easier to provide a list of indices instead of a slice, Brian therefore also allows for this syntax. Note that this is restricted to cases that are strictly equivalent with slicing syntax, e.g. you can write `G[[3, 4, 5]]` instead of `G[3:6]`, but you _cannot_ write `G[[3, 5, 7]]` or `G[[5, 4, 3]]`.

Subgroups can be used in most places where regular groups are used, e.g. their state variables or spiking activity can be recorded using monitors, they can be connected via [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses"), etc. In such situations, indices (e.g. the indices of the neurons to record from in a [`StateMonitor`](../reference/brian2.monitors.statemonitor.StateMonitor.html#brian2.monitors.statemonitor.StateMonitor "brian2.monitors.statemonitor.StateMonitor")) are relative to the subgroup, not to the main group

The following topics are not essential for beginners.

  

## Shared variables

Sometimes it can also be useful to introduce shared variables or subexpressions, i.e. variables that have a common value for all neurons. In contrast to external variables (such as `Cm` above), such variables can change during a run, e.g. by using [`run_regularly()`](../reference/brian2.groups.group.Group.html#brian2.groups.group.Group.run_regularly "brian2.groups.group.Group.run_regularly"). This can be for example used for an external stimulus that changes in the course of a run:
    
    
    >>> G = NeuronGroup(10, '''shared_input : volt (shared)
    ...                        dv/dt = (-v + shared_input)/tau : volt
    ...                        tau : second''', name='neurons')
    

Note that there are several restrictions around the use of shared variables: they cannot be written to in contexts where statements apply only to a subset of neurons (e.g. reset statements, see below). If a code block mixes statements writing to shared and vector variables, then the shared statements have to come first.

By default, subexpressions are re-evaluated whenever they are used, i.e. using a subexpression is completely equivalent to substituting it. Sometimes it is useful to instead only evaluate a subexpression once and then use this value for the rest of the time step. This can be achieved by using the `(constant over dt)` flag. This flag is mandatory for subexpressions that refer to stateful functions like `rand()` which notably allows them to be recorded with a [`StateMonitor`](../reference/brian2.monitors.statemonitor.StateMonitor.html#brian2.monitors.statemonitor.StateMonitor "brian2.monitors.statemonitor.StateMonitor") – otherwise the monitor would record a different instance of the random number than the one that was used in the equations.

For shared variables, setting by string expressions can only refer to shared values:
    
    
    >>> G.shared_input = '(4.0/N)*mV'
    >>> G.shared_input
    <neurons.shared_input: 0.4 * mvolt>
    

## Storing state variables

Sometimes it can be convenient to access multiple state variables at once, e.g. to set initial values from a dictionary of values or to store all the values of a group on disk. This can be done with the [`get_states()`](../reference/brian2.groups.group.VariableOwner.html#brian2.groups.group.VariableOwner.get_states "brian2.groups.group.VariableOwner.get_states") and [`set_states()`](../reference/brian2.groups.group.VariableOwner.html#brian2.groups.group.VariableOwner.set_states "brian2.groups.group.VariableOwner.set_states") methods:
    
    
    >>> group = NeuronGroup(5, '''dv/dt = -v/tau : 1
    ...                           tau : second''', name='neurons')
    >>> initial_values = {'v': [0, 1, 2, 3, 4],
    ...                   'tau': [10, 20, 10, 20, 10]*ms}
    >>> group.set_states(initial_values)
    >>> group.v[:]
    array([ 0.,  1.,  2.,  3.,  4.])
    >>> group.tau[:]
    array([ 10.,  20.,  10.,  20.,  10.]) * msecond
    >>> states = group.get_states()
    >>> states['v']
    array([ 0.,  1.,  2.,  3.,  4.])
    

The data (without physical units) can also be exported/imported to/from [Pandas](http://pandas.pydata.org/) data frames (needs an installation of `pandas`):
    
    
    >>> df = group.get_states(units=False, format='pandas')  
    >>> df  
       N      dt  i    t   tau    v
    0  5  0.0001  0  0.0  0.01  0.0
    1  5  0.0001  1  0.0  0.02  1.0
    2  5  0.0001  2  0.0  0.01  2.0
    3  5  0.0001  3  0.0  0.02  3.0
    4  5  0.0001  4  0.0  0.01  4.0
    >>> df['tau']  
    0    0.01
    1    0.02
    2    0.01
    3    0.02
    4    0.01
    Name: tau, dtype: float64
    >>> df['tau'] *= 2  
    >>> group.set_states(df[['tau']], units=False, format='pandas')  
    >>> group.tau  
    <neurons.tau: array([ 20.,  40.,  20.,  40.,  20.]) * msecond>
    

## Linked variables

A [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") can define parameters that are not stored in this group, but are instead a reference to a state variable in another group. For this, a group defines a parameter as `linked` and then uses [`linked_var()`](../reference/brian2.core.variables.linked_var.html#brian2.core.variables.linked_var "brian2.core.variables.linked_var") to specify the linking. This can for example be useful to model shared noise between cells:
    
    
    inp = NeuronGroup(1, 'dnoise/dt = -noise/tau + tau**-0.5*xi : 1')
    
    neurons = NeuronGroup(100, '''noise : 1 (linked)
                                  dv/dt = (-v + noise_strength*noise)/tau : volt''')
    neurons.noise = linked_var(inp, 'noise')
    

If the two groups have the same size, the linking will be done in a 1-to-1 fashion. If the source group has the size one (as in the above example) or if the source parameter is a shared variable, then the linking will be done as 1-to-all. In all other cases, you have to specify the indices to use for the linking explicitly:
    
    
    # two inputs with different phases
    inp = NeuronGroup(2, '''phase : 1
                            dx/dt = 1*mV/ms*sin(2*pi*100*Hz*t-phase) : volt''')
    inp.phase = [0, pi/2]
    
    neurons = NeuronGroup(100, '''inp : volt (linked)
                                  dv/dt = (-v + inp) / tau : volt''')
    # Half of the cells get the first input, other half gets the second
    neurons.inp = linked_var(inp, 'x', index=repeat([0, 1], 50))
    

## Time scaling of noise

Suppose we just had the differential equation

\\(dx/dt=\xi\\)

To solve this numerically, we could compute

\\(x(t+\mathrm{d}t)=x(t)+\xi_1\\)

where \\(\xi_1\\) is a normally distributed random number with mean 0 and standard deviation 1. However, what happens if we change the time step? Suppose we used a value of \\(\mathrm{d}t/2\\) instead of \\(\mathrm{d}t\\). Now, we compute

\\(x(t+\mathrm{d}t)=x(t+\mathrm{d}t/2)+\xi_1=x(t)+\xi_2+\xi_1\\)

The mean value of \\(x(t+\mathrm{d}t)\\) is 0 in both cases, but the standard deviations are different. The first method \\(x(t+\mathrm{d}t)=x(t)+\xi_1\\) gives \\(x(t+\mathrm{d}t)\\) a standard deviation of 1, whereas the second method \\(x(t+\mathrm{d}t)=x(t+\mathrm{d}/2)+\xi_1=x(t)+\xi_2+\xi_1\\) gives \\(x(t)\\) a variance of 1+1=2 and therefore a standard deviation of \\(\sqrt{2}\\).

In order to solve this problem, we use the rule \\(x(t+\mathrm{d}t)=x(t)+\sqrt{\mathrm{d}t}\xi_1\\), which makes the mean and standard deviation of the value at time \\(t\\) independent of \\(\mathrm{d}t\\). For this to make sense dimensionally, \\(\xi\\) must have units of `1/sqrt(second)`.

For further details, refer to a textbook on stochastic differential equations.

---

# Multi-threading with OpenMP2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/developer/openmp.html

# Multi-threading with OpenMP

The following is an outline of how to make C++ standalone templates compatible with OpenMP, and therefore make them work in a multi-threaded environment. This should be considered as an extension to [Code generation](codegen.html), that has to be read first. The C++ standalone mode of Brian is compatible with OpenMP, and therefore simulations can be launched by users with one or with multiple threads. Therefore, when adding new templates, the developers need to make sure that those templates are properly handling the situation if launched with OpenMP.

## Key concepts

All the simulations performed with the C++ standalone mode can be launched with multi-threading, and make use of multiple cores on the same machine. Basically, all the Brian operations that can easily be performed in parallel, such as computing the equations for [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup"), [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses"), and so on can and should be split among several threads. The network construction, so far, is still performed only by one single thread, and all created objects are shared by all the threads.

## Use of `#pragma` flags

In OpenMP, all the parallelism is handled thanks to extra comments, added in the main C++ code, under the form:
    
    
    #pragma omp ...
    

But to avoid any dependencies in the code that is generated by Brian when OpenMP is not activated, we are using functions that will only add those comments, during code generation, when such a multi-threading mode is turned on. By default, nothing will be inserted.

### Translations of the `#pragma` commands

All the translations from `openmp_pragma()` calls in the C++ templates are handled in the file `devices/cpp_standalone/codeobject.py` In this function, you can see that all calls with various string inputs will generate #pragma statements inserted into the C++ templates during code generation. For example:
    
    
    {{ openmp_pragma('static') }}
    

will be transformed, during code generation, into:
    
    
    #pragma omp for schedule(static)
    

You can find the list of all the translations in the core of the `openmp_pragma()` function, and if some extra translations are needed, they should be added here.

### Execution of the OpenMP code

In this section, we are explaining the main ideas behind the OpenMP mode of Brian, and how the simulation is executed in such a parallel context. As can be seen in `devices/cpp_standalone/templates/main.cpp`, the appropriate number of threads, defined by the user, is fixed at the beginning of the main function in the C++ code with:
    
    
    {{ openmp_pragma('set_num_threads') }}
    

equivalent to (thanks to the `openmp_pragam()` function defined above): nothing if OpenMP is turned off (default), and to:
    
    
    omp_set_dynamic(0);
    omp_set_num_threads(nb_threads);
    

otherwise. When OpenMP creates a parallel context, this is the number of threads that will be used. As said, network creation is performed without any calls to OpenMP, on one single thread. Each template that wants to use parallelism has to add `{{ openmp_pragma{('parallel')}}` to create a general block that will be executed in parallel or `{{ openmp_pragma{('parallel-static')}}` to execute a single loop in parallel.

## How to make your template use OpenMP parallelism

To design a parallel template, such as for example `devices/cpp_standalone/templates/common_group.cpp`, you can see that as soon as you have loops that can safely be split across nodes, you just need to add an openmp command in front of those loops:
    
    
    {{openmp_pragma('parallel-static')}}
    for(int _idx=0; _idx<N; _idx++)
    {
        ...
    }
    

By doing so, OpenMP will take care of splitting the indices and each thread will loop only on a subset of indices, sharing the load. By default, the scheduling use for splitting the indices is static, meaning that each node will get the same number of indices: this is the faster scheduling in OpenMP, and it makes sense for [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") or [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses") because operations are the same for all indices. By having a look at examples of templates such as `devices/cpp_standalone/templates/statemonitor.cpp`, you can see that you can merge portions of code executed by only one node and portions executed in parallel. In this template, for example, only one node is recording the time and extending the size of the arrays to store the recorded values:
    
    
    {{_dynamic_t}}.push_back(_clock_t);
    
    // Resize the dynamic arrays
    {{_recorded}}.resize(_new_size, _num_indices);
    

But then, values are written in the arrays by all the nodes:
    
    
    {{ openmp_pragma('parallel-static') }}
    for (int _i = 0; _i < _num_indices; _i++)
    {
        ....
    }
    

In general, operations that manipulate global data structures, e.g. that use `push_back` for a `std::vector`, should only be executed by a single thread.

## Synaptic propagation in parallel

### General ideas

With OpenMP, synaptic propagation is also multi-threaded. Therefore, we have to modify the `SynapticPathway` objects, handling spike propagation. As can be seen in `devices/cpp_standalone/templates/synapses_classes.cpp`, such an object, created during run time, will be able to get the number of threads decided by the user:
    
    
    _nb_threads = {{ openmp_pragma('get_num_threads') }};
    

By doing so, a `SynapticPathway`, instead of handling only one `SpikeQueue`, will be divided into `_nb_threads` `SpikeQueue`s, each of them handling a subset of the total number of connections. All the calls to `SynapticPathway` object are performed from within `parallel` blocks in the `synapses` and `synapses_push_spikes` template, we have to take this parallel context into account. This is why all the function of the `SynapticPathway` object are taking care of the node number:
    
    
    void push(int *spikes, unsigned int nspikes)
    {
        queue[{{ openmp_pragma('get_thread_num') }}]->push(spikes, nspikes);
    }
    

Such a method for the `SynapticPathway` will make sure that when spikes are propagated, all the threads will propagate them to their connections. By default, again, if OpenMP is turned off, the queue vector has size 1.

### Preparation of the `SynapticPathway`

Here we are explaining the implementation of the `prepare()` method for `SynapticPathway`:
    
    
    {{ openmp_pragma('parallel') }}
    {
        unsigned int length;
        if ({{ openmp_pragma('get_thread_num') }} == _nb_threads - 1)
            length = n_synapses - (unsigned int) {{ openmp_pragma('get_thread_num') }}*n_synapses/_nb_threads;
        else
            length = (unsigned int) n_synapses/_nb_threads;
    
        unsigned int padding  = {{ openmp_pragma('get_thread_num') }}*(n_synapses/_nb_threads);
    
        queue[{{ openmp_pragma('get_thread_num') }}]->openmp_padding = padding;
        queue[{{ openmp_pragma('get_thread_num') }}]->prepare(&real_delays[padding], &sources[padding], length, _dt);
    }
    

Basically, each threads is getting an equal number of synapses (except the last one, that will get the remaining ones, if the number is not a multiple of `n_threads`), and the queues are receiving a padding integer telling them what part of the synapses belongs to each queue. After that, the parallel context is destroyed, and network creation can continue. Note that this could have been done without a parallel context, in a sequential manner, but this is just speeding up everything.

### Selection of the spikes

Here we are explaining the implementation of the `peek()` method for `SynapticPathway`. This is an example of concurrent access to data structures that are not well handled in parallel, such as `std::vector`. When `peek()` is called, we need to return a vector of all the neuron spiking at that particular time. Therefore, we need to ask every queue of the `SynapticPathway` what are the id of the spiking neurons, and concatenate them. Because those ids are stored in vectors with various shapes, we need to loop over nodes to perform this concatenate, in a sequential manner:
    
    
    {{ openmp_pragma('static-ordered') }}
    for(int _thread=0; _thread < {{ openmp_pragma('get_num_threads') }}; _thread++)
    {
        {{ openmp_pragma('ordered') }}
        {
            if (_thread == 0)
                all_peek.clear();
            all_peek.insert(all_peek.end(), queue[_thread]->peek()->begin(), queue[_thread]->peek()->end());
        }
    }
    

The loop, with the keyword ‘static-ordered’, is therefore performed such that node 0 enters it first, then node 1, and so on. Only one node at a time is executing the block statement. This is needed because vector manipulations can not be performed in a multi-threaded manner. At the end of the loop, `all_peek` is now a vector where all sub queues have written the id of spiking cells, and therefore this is the list of all spiking cells within the `SynapticPathway`.

## Compilation of the code

One extra file needs to be modified, in order for OpenMP implementation to work. This is the makefile `devices/cpp_standalone/templates/makefile`. As one can simply see, the CFLAGS are dynamically modified during code generation thanks to:
    
    
    {{ openmp_pragma('compilation') }}
    

If OpenMP is activated, this will add the following dependencies:
    
    
    -fopenmp
    

such that if OpenMP is turned off, nothing, in the generated code, does depend on it.

---

# Multicompartment models2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/user/multicompartmental.html

# Multicompartment models

For Brian 1 users

See the document [Multicompartmental models (Brian 1 –> 2 conversion)](../introduction/brian1_to_2/multicompartmental.html) for details how to convert Brian 1 code.

It is possible to create neuron models with a spatially extended morphology, using the [`SpatialNeuron`](../reference/brian2.spatialneuron.spatialneuron.SpatialNeuron.html#brian2.spatialneuron.spatialneuron.SpatialNeuron "brian2.spatialneuron.spatialneuron.SpatialNeuron") class. A [`SpatialNeuron`](../reference/brian2.spatialneuron.spatialneuron.SpatialNeuron.html#brian2.spatialneuron.spatialneuron.SpatialNeuron "brian2.spatialneuron.spatialneuron.SpatialNeuron") is a single neuron with many compartments. Essentially, it works as a [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") where elements are compartments instead of neurons.

A [`SpatialNeuron`](../reference/brian2.spatialneuron.spatialneuron.SpatialNeuron.html#brian2.spatialneuron.spatialneuron.SpatialNeuron "brian2.spatialneuron.spatialneuron.SpatialNeuron") is specified by a morphology (see Creating a neuron morphology) and a set of equations for transmembrane currents (see Creating a spatially extended neuron).

## Creating a neuron morphology

### Schematic morphologies

Morphologies can be created combining geometrical objects:
    
    
    soma = Soma(diameter=30*um)
    cylinder = Cylinder(diameter=1*um, length=100*um, n=10)
    

The first statement creates a single iso-potential compartment (i.e. with no axial resistance within the compartment), with its area calculated as the area of a sphere with the given diameter. The second one specifies a cylinder consisting of 10 compartments with identical diameter and the given total length.

For more precise control over the geometry, you can specify the length and diameter of each individual compartment, including the diameter at the start of the section (i.e. for `n` compartments: `n` length and `n+1` diameter values) in a [`Section`](../reference/brian2.spatialneuron.morphology.Section.html#brian2.spatialneuron.morphology.Section "brian2.spatialneuron.morphology.Section") object:
    
    
    section = Section(diameter=[6, 5, 4, 3, 2, 1]*um, length=[10, 10, 10, 5, 5]*um, n=5)
    

The individual compartments are modeled as truncated cones, changing the diameter linearly between the given diameters over the length of the compartment. Note that the `diameter` argument specifies the values at the nodes _between_ the compartments, but accessing the `diameter` attribute of a [`Morphology`](../reference/brian2.spatialneuron.morphology.Morphology.html#brian2.spatialneuron.morphology.Morphology "brian2.spatialneuron.morphology.Morphology") object will return the diameter at the _center_ of the compartment (see the note below).

The following table summarizes the different options to create schematic morphologies (the black compartment before the start of the section represents the parent compartment with diameter 15 μm, not specified in the code below):

| **Example**  
---|---  
**Soma** | 

> 
>     # Soma always has a single compartment
>     Soma(diameter=30*um)
>     

![../_images/soma.svg](../_images/soma.svg)  
**Cylinder** | 

> 
>     # Each compartment has fixed length and diameter
>     Cylinder(n=5, diameter=10*um, length=50*um)
>     

![../_images/cylinder.svg](../_images/cylinder.svg)  
**Section** | 

> 
>     # Length and diameter individually defined for each compartment (at start
>     # and end)
>     Section(n=5, diameter=[15, 5, 10, 5, 10, 5]*um,
>             length=[10, 20, 5, 5, 10]*um)
>     

![../_images/section.svg](../_images/section.svg)  
  
Note

For a [`Section`](../reference/brian2.spatialneuron.morphology.Section.html#brian2.spatialneuron.morphology.Section "brian2.spatialneuron.morphology.Section"), the `diameter` argument specifies the diameter _between_ the compartments (and at the beginning/end of the first/last compartment). the corresponding values can therefore be later retrieved from the [`Morphology`](../reference/brian2.spatialneuron.morphology.Morphology.html#brian2.spatialneuron.morphology.Morphology "brian2.spatialneuron.morphology.Morphology") via the `start_diameter` and `end_diameter` attributes. The `diameter` attribute of a [`Morphology`](../reference/brian2.spatialneuron.morphology.Morphology.html#brian2.spatialneuron.morphology.Morphology "brian2.spatialneuron.morphology.Morphology") does correspond to the diameter at the midpoint of the compartment. For a [`Cylinder`](../reference/brian2.spatialneuron.morphology.Cylinder.html#brian2.spatialneuron.morphology.Cylinder "brian2.spatialneuron.morphology.Cylinder"), `start_diameter`, `diameter`, and `end_diameter` are of course all identical.

The tree structure of a morphology is created by attaching [`Morphology`](../reference/brian2.spatialneuron.morphology.Morphology.html#brian2.spatialneuron.morphology.Morphology "brian2.spatialneuron.morphology.Morphology") objects together:
    
    
    morpho = Soma(diameter=30*um)
    morpho.axon = Cylinder(length=100*um, diameter=1*um, n=10)
    morpho.dendrite = Cylinder(length=50*um, diameter=2*um, n=5)
    

These statements create a morphology consisting of a cylindrical axon and a dendrite attached to a spherical soma. Note that the names `axon` and `dendrite` are arbitrary and chosen by the user. For example, the same morphology can be created as follows:
    
    
    morpho = Soma(diameter=30*um)
    morpho.output_process = Cylinder(length=100*um, diameter=1*um, n=10)
    morpho.input_process = Cylinder(length=50*um, diameter=2*um, n=5)
    

The syntax is recursive, for example two sections can be added at the end of the dendrite as follows:
    
    
    morpho.dendrite.branch1 = Cylinder(length=50*um, diameter=1*um, n=3)
    morpho.dendrite.branch2 = Cylinder(length=50*um, diameter=1*um, n=3)
    

Equivalently, one can use an indexing syntax:
    
    
    morpho['dendrite']['branch1'] = Cylinder(length=50*um, diameter=1*um, n=3)
    morpho['dendrite']['branch2'] = Cylinder(length=50*um, diameter=1*um, n=3)
    

The names given to sections are completely up to the user. However, names that consist of a single digit (`1` to `9`) or the letters `L` (for left) and `R` (for right) allow for a special short syntax: they can be joined together directly, without the needs for dots (or dictionary syntax) and therefore allow to quickly navigate through the morphology tree (e.g. `morpho.LRLLR` is equivalent to `morpho.L.R.L.L.R`). This short syntax can also be used to create trees:
    
    
    >>> morpho = Soma(diameter=30*um)
    >>> morpho.L = Cylinder(length=10*um, diameter=1*um, n=3)
    >>> morpho.L1 = Cylinder(length=5*um, diameter=1*um, n=3)
    >>> morpho.L2 = Cylinder(length=5*um, diameter=1*um, n=3)
    >>> morpho.L3 = Cylinder(length=5*um, diameter=1*um, n=3)
    >>> morpho.R = Cylinder(length=10*um, diameter=1*um, n=3)
    >>> morpho.RL = Cylinder(length=5*um, diameter=1*um, n=3)
    >>> morpho.RR = Cylinder(length=5*um, diameter=1*um, n=3)
    

The above instructions create a dendritic tree with two main sections, three sections attached to the first section and two to the second. This can be verified with the [`Morphology.topology`](../reference/brian2.spatialneuron.morphology.Morphology.html#brian2.spatialneuron.morphology.Morphology.topology "brian2.spatialneuron.morphology.Morphology.topology") method:
    
    
    >>> morpho.topology()  
    ( )  [root]
       `---|  .L
            `---|  .L.1
            `---|  .L.2
            `---|  .L.3
       `---|  .R
            `---|  .R.L
            `---|  .R.R
    

Note that an expression such as `morpho.L` will always refer to the entire subtree. However, accessing the attributes (e.g. `diameter`) will only return the values for the given section.

Note

To avoid ambiguities, do not use names for sections that can be interpreted in the abbreviated way detailed above. For example, do not name a child section `L1` (which will be interpreted as the first child of the child `L`)

The number of compartments in a section can be accessed with `morpho.n` (or `morpho.L.n`, etc.), the number of total sections and compartments in a subtree can be accessed with `morpho.total_sections` and `morpho.total_compartments` respectively.

#### Adding coordinates

For plotting purposes, it can be useful to add coordinates to a [`Morphology`](../reference/brian2.spatialneuron.morphology.Morphology.html#brian2.spatialneuron.morphology.Morphology "brian2.spatialneuron.morphology.Morphology") that was created using the “schematic” approach described above. This can be done by calling the `generate_coordinates` method on a morphology, which will return an identical morphology but with additional 2D or 3D coordinates. By default, this method creates a morphology according to a deterministic algorithm in 2D:
    
    
    new_morpho = morpho.generate_coordinates()
    

![../_images/morphology_deterministic_coords.png](../_images/morphology_deterministic_coords.png)

To get more “realistic” morphologies, this function can also be used to create morphologies in 3D where the orientation of each section differs from the orientation of the parent section by a random amount:
    
    
    new_morpho = morpho.generate_coordinates(section_randomness=25)
    

![../_images/morphology_random_section_1.png](../_images/morphology_random_section_1.png) | ![../_images/morphology_random_section_2.png](../_images/morphology_random_section_2.png) | ![../_images/morphology_random_section_3.png](../_images/morphology_random_section_3.png)  
---|---|---  
  
This algorithm will base the orientation of each section on the orientation of the parent section and then randomly perturb this orientation. More precisely, the algorithm first chooses a random vector orthogonal to the orientation of the parent section. Then, the section will be rotated around this orthogonal vector by a random angle, drawn from an exponential distribution with the \\(\beta\\) parameter (in degrees) given by `section_randomness`. This \\(\beta\\) parameter specifies both the mean and the standard deviation of the rotation angle. Note that no maximum rotation angle is enforced, values for `section_randomness` should therefore be reasonably small (e.g. using a `section_randomness` of `45` would already lead to a probability of ~14% that the section will be rotated by more than 90 degrees, therefore making the section go “backwards”).

In addition, also the orientation of each compartment within a section can be randomly varied:
    
    
    new_morpho = morpho.generate_coordinates(section_randomness=25,
                                             compartment_randomness=15)
    

![../_images/morphology_random_section_compartment_1.png](../_images/morphology_random_section_compartment_1.png) | ![../_images/morphology_random_section_compartment_2.png](../_images/morphology_random_section_compartment_2.png) | ![../_images/morphology_random_section_compartment_3.png](../_images/morphology_random_section_compartment_3.png)  
---|---|---  
  
The algorithm is the same as the one presented above, but applied individually to each compartment within a section (still based on the orientation on the parent _section_ , not on the orientation of the previous _compartment_).

### Complex morphologies

Morphologies can also be created from information about the compartment coordinates in 3D space. Such morphologies can be loaded from a `.swc` file (a standard format for neuronal morphologies; for a large database of morphologies in this format see <http://neuromorpho.org>):
    
    
    morpho = Morphology.from_file('corticalcell.swc')
    

To manually create a morphology from a list of points in a similar format to SWC files, see [`Morphology.from_points`](../reference/brian2.spatialneuron.morphology.Morphology.html#brian2.spatialneuron.morphology.Morphology.from_points "brian2.spatialneuron.morphology.Morphology.from_points").

Morphologies that are created in such a way will use standard names for the sections that allow for the short syntax shown in the previous sections: if a section has one or two child sections, then they will be called `L` and `R`, otherwise they will be numbered starting at `1`.

Morphologies with coordinates can also be created section by section, following the same syntax as for “schematic” morphologies:
    
    
    soma = Soma(diameter=30*um, x=50*um, y=20*um)
    cylinder = Cylinder(n=10, x=[0, 100]*um, diameter=1*um)
    section = Section(n=5,
                      x=[0, 10, 20, 30, 40, 50]*um,
                      y=[0, 10, 20, 30, 40, 50]*um,
                      z=[0, 10, 10, 10, 10, 10]*um,
                      diameter=[6, 5, 4, 3, 2, 1]*um)
    

Note that the `x`, `y`, `z` attributes of [`Morphology`](../reference/brian2.spatialneuron.morphology.Morphology.html#brian2.spatialneuron.morphology.Morphology "brian2.spatialneuron.morphology.Morphology") and [`SpatialNeuron`](../reference/brian2.spatialneuron.spatialneuron.SpatialNeuron.html#brian2.spatialneuron.spatialneuron.SpatialNeuron "brian2.spatialneuron.spatialneuron.SpatialNeuron") will return the coordinates at the midpoint of each compartment (as for all other attributes that vary over the length of a compartment, e.g. `diameter` or `distance`), but during construction the coordinates refer to the start and end of the section ([`Cylinder`](../reference/brian2.spatialneuron.morphology.Cylinder.html#brian2.spatialneuron.morphology.Cylinder "brian2.spatialneuron.morphology.Cylinder")), respectively to the coordinates of the nodes between the compartments ([`Section`](../reference/brian2.spatialneuron.morphology.Section.html#brian2.spatialneuron.morphology.Section "brian2.spatialneuron.morphology.Section")).

A few additional remarks:

  1. In the majority of simulations, coordinates are not used in the neuronal equations, therefore the coordinates are purely for visualization purposes and do not affect the simulation results in any way.

  2. Coordinate specification cannot be combined with length specification – lengths are automatically calculated from the coordinates.

  3. The coordinate specification can also be 1- or 2-dimensional (as in the first two examples above), the unspecified coordinate will use 0 μm.

  4. All coordinates are interpreted relative to the parent compartment, i.e. the point (0 μm, 0 μm, 0 μm) refers to the end point of the previous compartment. Most of the time, the first element of the coordinate specification is therefore 0 μm, to continue a section where the previous one ended. However, it can be convenient to use a value different from 0 μm for sections connecting to the [`Soma`](../reference/brian2.spatialneuron.morphology.Soma.html#brian2.spatialneuron.morphology.Soma "brian2.spatialneuron.morphology.Soma") to make them (visually) connect to a point on the sphere surface instead of the center of the sphere.

## Creating a spatially extended neuron

A [`SpatialNeuron`](../reference/brian2.spatialneuron.spatialneuron.SpatialNeuron.html#brian2.spatialneuron.spatialneuron.SpatialNeuron "brian2.spatialneuron.spatialneuron.SpatialNeuron") is a spatially extended neuron. It is created by specifying the morphology as a [`Morphology`](../reference/brian2.spatialneuron.morphology.Morphology.html#brian2.spatialneuron.morphology.Morphology "brian2.spatialneuron.morphology.Morphology") object, the equations for transmembrane currents, and optionally the specific membrane capacitance `Cm` and intracellular resistivity `Ri`:
    
    
    gL = 1e-4*siemens/cm**2
    EL = -70*mV
    eqs = '''
    Im=gL * (EL - v) : amp/meter**2
    I : amp (point current)
    '''
    neuron = SpatialNeuron(morphology=morpho, model=eqs, Cm=1*uF/cm**2, Ri=100*ohm*cm)
    neuron.v = EL + 10*mV
    

Several state variables are created automatically: the [`SpatialNeuron`](../reference/brian2.spatialneuron.spatialneuron.SpatialNeuron.html#brian2.spatialneuron.spatialneuron.SpatialNeuron "brian2.spatialneuron.spatialneuron.SpatialNeuron") inherits all the geometrical variables of the compartments (`length`, `diameter`, `area`, `volume`), as well as the `distance` variable that gives the distance to the soma. For morphologies that use coordinates, the `x`, `y` and `z` variables are provided as well. Additionally, a state variable `Cm` is created. It is initialized with the value given at construction, but it can be modified on a compartment per compartment basis (which is useful to model myelinated axons). The membrane potential is stored in state variable `v`.

Note that for all variable values that vary across a compartment (e.g. `distance`, `x`, `y`, `z`, `v`), the value that is reported is the value at the midpoint of the compartment.

The key state variable, which must be specified at construction, is `Im`. It is the total transmembrane current, expressed in units of current per area. This is a mandatory line in the definition of the model. The rest of the string description may include other state variables (differential equations or subexpressions) or parameters, exactly as in [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup"). At every timestep, Brian integrates the state variables, calculates the transmembrane current at every point on the neuronal morphology, and updates `v` using the transmembrane current and the diffusion current, which is calculated based on the morphology and the intracellular resistivity. Note that the transmembrane current is a surfacic current, not the total current in the compartment. This choice means that the model equations are independent of the number of compartments chosen for the simulation. The space and time constants can obtained for any point of the neuron with the `space_constant` respectively `time_constant` attributes:
    
    
    l = neuron.space_constant[0]
    tau = neuron.time_constant[0]
    

The calculation is based on the local total conductance (not just the leak conductance), therefore, it can potentially vary during a simulation (e.g. decrease during an action potential). The reported value is only correct for compartments with a cylindrical geometry, though, it does not give reasonable values for compartments with strongly varying diameter.

To inject a current `I` at a particular point (e.g. through an electrode or a synapse), this current must be divided by the area of the compartment when inserted in the transmembrane current equation. This is done automatically when the flag `point current` is specified, as in the example above. This flag can apply only to subexpressions or parameters with amp units. Internally, the expression of the transmembrane current `Im` is simply augmented with `+I/area`. A current can then be injected in the first compartment of the neuron (generally the soma) as follows:
    
    
    neuron.I[0] = 1*nA
    

State variables of the [`SpatialNeuron`](../reference/brian2.spatialneuron.spatialneuron.SpatialNeuron.html#brian2.spatialneuron.spatialneuron.SpatialNeuron "brian2.spatialneuron.spatialneuron.SpatialNeuron") include all the compartments of that neuron (including subtrees). Therefore, the statement `neuron.v = EL + 10*mV` sets the membrane potential of the entire neuron at -60 mV.

Subtrees can be accessed by attribute (in the same way as in [`Morphology`](../reference/brian2.spatialneuron.morphology.Morphology.html#brian2.spatialneuron.morphology.Morphology "brian2.spatialneuron.morphology.Morphology") objects):
    
    
    neuron.axon.gNa = 10*gL
    

Note that the state variables correspond to the entire subtree, not just the main section. That is, if the axon had branches, then the above statement would change `gNa` on the main section and all the sections in the subtree. To access the main section only, use the attribute `main`:
    
    
    neuron.axon.main.gNa = 10*gL
    

A typical use case is when one wants to change parameter values at the soma only. For example, inserting an electrode current at the soma is done as follows:
    
    
    neuron.main.I = 1*nA
    

A part of a section can be accessed as follows:
    
    
    initial_segment = neuron.axon[10*um:50*um]
    

Finally, similar to the way that you can refer to a subset of neurons of a [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup"), you can also index the [`SpatialNeuron`](../reference/brian2.spatialneuron.spatialneuron.SpatialNeuron.html#brian2.spatialneuron.spatialneuron.SpatialNeuron "brian2.spatialneuron.spatialneuron.SpatialNeuron") object itself, e.g. to get a group representing only the first compartment of a cell (typically the soma), you can use:
    
    
    soma = neuron[0]
    

In the same way as for sections, you can also use slices, either with the indices of compartments, or with the distance from the root:
    
    
    first_compartments = neuron[:3]
    first_compartments = neuron[0*um:30*um]
    

However, note that this is restricted to contiguous indices which most of the time means that all compartments indexed in this way have to be part of the same section. Such indices can be acquired directly from the morphology:
    
    
    axon = neuron[morpho.axon.indices[:]]
    

or, more concisely:
    
    
    axon = neuron[morpho.axon]
    

### Synaptic inputs

There are two methods to have synapses on [`SpatialNeuron`](../reference/brian2.spatialneuron.spatialneuron.SpatialNeuron.html#brian2.spatialneuron.spatialneuron.SpatialNeuron "brian2.spatialneuron.spatialneuron.SpatialNeuron"). The first one to insert synaptic equations directly in the neuron equations:
    
    
    eqs='''
    Im = gL * (EL - v) : amp/meter**2
    Is = gs * (Es - v) : amp (point current)
    dgs/dt = -gs/taus : siemens
    '''
    neuron = SpatialNeuron(morphology=morpho, model=eqs, Cm=1*uF/cm**2, Ri=100*ohm*cm)
    

Note that, as for electrode stimulation, the synaptic current must be defined as a point current. Then we use a [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses") object to connect a spike source to the neuron:
    
    
    S = Synapses(stimulation, neuron, on_pre='gs += w')
    S.connect(i=0, j=50)
    S.connect(i=1, j=100)
    

This creates two synapses, on compartments 50 and 100. One can specify the compartment number with its spatial position by indexing the morphology:
    
    
    S.connect(i=0, j=morpho[25*um])
    S.connect(i=1, j=morpho.axon[30*um])
    

In this method for creating synapses, there is a single value for the synaptic conductance in any compartment. This means that it will fail if there are several synapses onto the same compartment and synaptic equations are nonlinear. The second method, which works in such cases, is to have synaptic equations in the [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses") object:
    
    
    eqs='''
    Im = gL * (EL - v) : amp/meter**2
    Is = gs * (Es - v) : amp (point current)
    gs : siemens
    '''
    neuron = SpatialNeuron(morphology=morpho, model=eqs, Cm=1 * uF / cm ** 2, Ri=100 * ohm * cm)
    S = Synapses(stimulation, neuron, model='''dg/dt = -g/taus : siemens
                                               gs_post = g : siemens (summed)''',
                 on_pre='g += w')
    

Here each synapse (instead of each compartment) has an associated value `g`, and all values of `g` for each compartment (i.e., all synapses targeting that compartment) are collected into the compartmental variable `gs`.

### Detecting spikes

To detect and record spikes, we must specify a threshold condition, essentially in the same way as for a [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup"):
    
    
    neuron = SpatialNeuron(morphology=morpho, model=eqs, threshold='v > 0*mV', refractory='v > -10*mV')
    

Here spikes are detected when the membrane potential `v` reaches 0 mV. Because there is generally no explicit reset in this type of model (although it is possible to specify one), `v` remains above 0 mV for some time. To avoid detecting spikes during this entire time, we specify a refractory period. In this case no spike is detected as long as `v` is greater than -10 mV. Another possibility could be:
    
    
    neuron = SpatialNeuron(morphology=morpho, model=eqs, threshold='m > 0.5', refractory='m > 0.4')
    

where `m` is the state variable for sodium channel activation (assuming this has been defined in the model). Here a spike is detected when half of the sodium channels are open.

With the syntax above, spikes are detected in all compartments of the neuron. To detect them in a single compartment, use the `threshold_location` keyword:
    
    
    neuron = SpatialNeuron(morphology=morpho, model=eqs, threshold='m > 0.5', threshold_location=30,
                           refractory='m > 0.4')
    

In this case, spikes are only detecting in compartment number 30. Reset then applies locally to that compartment (if a reset statement is defined). Again the location of the threshold can be specified with spatial position:
    
    
    neuron = SpatialNeuron(morphology=morpho, model=eqs, threshold='m > 0.5',
                           threshold_location=morpho.axon[30*um],
                           refractory='m > 0.4')
    

### Subgroups

In the same way that you can refer to a subset of neurons in a [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup"), you can also refer to a subset of compartments in a [`SpatialNeuron`](../reference/brian2.spatialneuron.spatialneuron.SpatialNeuron.html#brian2.spatialneuron.spatialneuron.SpatialNeuron "brian2.spatialneuron.spatialneuron.SpatialNeuron")

---

# Namespaces2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/advanced/namespaces.html

# Namespaces

[`Equations`](../reference/brian2.equations.equations.Equations.html#brian2.equations.equations.Equations "brian2.equations.equations.Equations") can contain references to external parameters or functions. During the initialisation of a [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") or a [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses") object, this _namespace_ can be provided as an argument. This is a group-specific namespace that will only be used for names in the context of the respective group. Note that units and a set of standard functions are always provided and should not be given explicitly. This namespace does not necessarily need to be exhaustive at the time of the creation of the [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup")/[`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses"), entries can be added (or modified) at a later stage via the `namespace` attribute (e.g. `G.namespace['tau'] = 10*ms`).

At the point of the call to the [`Network.run`](../reference/brian2.core.network.Network.html#brian2.core.network.Network.run "brian2.core.network.Network.run") namespace, any group-specific namespace will be augmented by the “run namespace”. This namespace can be either given explicitly as an argument to the `run` method or it will be taken from the locals and globals surrounding the call. A warning will be emitted if a name is defined in more than one namespace.

To summarize: an external identifier will be looked up in the context of an object such as [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") or [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses"). It will follow the following resolution hierarchy:

  1. Default unit and function names.

  2. Names defined in the explicit group-specific namespace.

  3. Names in the run namespace which is either explicitly given or the implicit namespace surrounding the run call.

Note that if you completely specify your namespaces at the [`Group`](../reference/brian2.groups.group.Group.html#brian2.groups.group.Group "brian2.groups.group.Group") level, you should probably pass an empty dictionary as the namespace argument to the `run` call – this will completely switch off the “implicit namespace” mechanism.

The following three examples show the different ways of providing external variable values, all having the same effect in this case:
    
    
    # Explicit argument to the NeuronGroup
    G = NeuronGroup(1, 'dv/dt = -v / tau : 1', namespace={'tau': 10*ms})
    net = Network(G)
    net.run(10*ms)
    
    # Explicit argument to the run function
    G = NeuronGroup(1, 'dv/dt = -v / tau : 1')
    net = Network(G)
    net.run(10*ms, namespace={'tau': 10*ms})
    
    # Implicit namespace from the context
    G = NeuronGroup(1, 'dv/dt = -v / tau : 1')
    net = Network(G)
    tau = 10*ms
    net.run(10*ms)
    

External variables are free to change between runs (but not during one run), the value at the time of the [`run()`](../reference/brian2.core.magic.run.html#brian2.core.magic.run "brian2.core.magic.run") call is used in the simulation.

---

# Older notes on code generation2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/developer/oldcodegen.html

# Older notes on code generation

The following is an outline of how the Brian 2 code generation system works, with indicators as to which packages to look at and which bits of code to read for a clearer understanding.

We illustrate the global process with an example, the creation and running of a single [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") object:

  * Parse the equations, add refractoriness to them: this isn’t really part of code generation.

  * Allocate memory for the state variables.

  * Create `Thresholder`, `Resetter` and `StateUpdater` objects.

    * Determine all the variable and function names used in the respective abstract code blocks and templates

    * Determine the abstract namespace, i.e. determine a `Variable` or [`Function`](../reference/brian2.core.functions.Function.html#brian2.core.functions.Function "brian2.core.functions.Function") object for each name.

    * Create a `CodeObject` based on the abstract code, template and abstract namespace. This will generate code in the target language and the namespace in which the code will be executed.

  * At runtime, each object calls `CodeObject.__call__` to execute the code.

## Stages of code generation

### Equations to abstract code

In the case of [`Equations`](../reference/brian2.equations.equations.Equations.html#brian2.equations.equations.Equations "brian2.equations.equations.Equations"), the set of equations are combined with a numerical integration method to generate an _abstract code block_ (see below) which represents the integration code for a single time step.

An example of this would be converting the following equations:
    
    
    eqs = '''
    dv/dt = (v0-v)/tau : volt (unless refractory)
    v0 : volt
    '''
    group = NeuronGroup(N, eqs, threshold='v>10*mV',
                        reset='v=0*mV', refractory=5*ms)
    

into the following abstract code using the [`exponential_euler`](../reference/brian2.stateupdaters.exponential_euler.exponential_euler.html#brian2.stateupdaters.exponential_euler.exponential_euler "brian2.stateupdaters.exponential_euler.exponential_euler") method (which is selected automatically):
    
    
    not_refractory = 1*((t - lastspike) > 0.005000)
    _BA_v = -v0
    _v = -_BA_v + (_BA_v + v)*exp(-dt*not_refractory/tau)
    v = _v
    

The code for this stage can be seen in `NeuronGroup.__init__`, `StateUpdater.__init__`, and `StateUpdater.update_abstract_code` (in `brian2.groups.neurongroup`), and the [`StateUpdateMethod`](../reference/brian2.stateupdaters.base.StateUpdateMethod.html#brian2.stateupdaters.base.StateUpdateMethod "brian2.stateupdaters.base.StateUpdateMethod") classes defined in the `brian2.stateupdaters` package.

For more details, see [State update](../advanced/state_update.html).

### Abstract code

‘Abstract code’ is just a multi-line string representing a block of code which should be executed for each item (e.g. each neuron, each synapse). Each item is independent of the others in abstract code. This allows us to later generate code either for vectorised languages (like numpy in Python) or using loops (e.g. in C++).

Abstract code is parsed according to Python syntax, with certain language constructs excluded. For example, there cannot be any conditional or looping statements at the moment, although support for this is in principle possible and may be added later. Essentially, all that is allowed at the moment is a sequence of arithmetical `a = b*c` style statements.

Abstract code is provided directly by the user for threshold and reset statements in [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") and for pre/post spiking events in [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses").

### Abstract code to snippet

We convert abstract code into a ‘snippet’, which is a small segment of code which is syntactically correct in the target language, although it may not be runnable on its own (that’s handled by insertion into a ‘template’ later). This is handled by the `CodeGenerator` object in `brian2.codegen.generators`. In the case of converting into python/numpy code this typically doesn’t involve any changes to the code at all because the original code is in Python syntax. For conversion to C++, we have to do some syntactic transformations (e.g. `a**b` is converted to `pow(a, b)`), and add declarations for certain variables (e.g. converting `x=y*z` into `const double x = y*z;`).

An example of a snippet in C++ for the equations above:
    
    
    const double v0 = _ptr_array_neurongroup_v0[_neuron_idx];
    const double lastspike = _ptr_array_neurongroup_lastspike[_neuron_idx];
    bool not_refractory = _ptr_array_neurongroup_not_refractory[_neuron_idx];
    double v = _ptr_array_neurongroup_v[_neuron_idx];
    not_refractory = 1 * (t - lastspike > 0.0050000000000000001);
    const double _BA_v = -(v0);
    const double _v = -(_BA_v) + (_BA_v + v) * exp(-(dt) * not_refractory / tau);
    v = _v;
    _ptr_array_neurongroup_not_refractory[_neuron_idx] = not_refractory;
    _ptr_array_neurongroup_v[_neuron_idx] = v;
    

The code path that includes snippet generation will be discussed in more detail below, since it involves the concepts of namespaces and variables which we haven’t covered yet.

### Snippet to code block

The final stage in the generation of a runnable code block is the insertion of a snippet into a template. These use the Jinja2 template specification language. This is handled in `brian2.codegen.templates`.

An example of a template for Python thresholding:
    
    
    # USES_VARIABLES { not_refractory, lastspike, t }
    {% for line in code_lines %}
    {{line}}
    {% endfor %}
    _return_values, = _cond.nonzero()
    # Set the neuron to refractory
    not_refractory[_return_values] = False
    lastspike[_return_values] = t
    

and the output code from the example equations above:
    
    
    # USES_VARIABLES { not_refractory, lastspike, t }
    v = _array_neurongroup_v
    _cond = v > 10 * mV
    _return_values, = _cond.nonzero()
    # Set the neuron to refractory
    not_refractory[_return_values] = False
    lastspike[_return_values] = t
    

### Code block to executing code

A code block represents runnable code. Brian operates in two different regimes, either in runtime or standalone mode. In runtime mode, memory allocation and overall simulation control is handled by Python and numpy, and code objects operate on this memory when called directly by Brian. This is the typical way that Brian is used, and it allows for a rapid development cycle. However, we also support a standalone mode in which an entire project workspace is generated for a target language or device by Brian, which can then be compiled and run independently of Brian. Each mode has different templates, and does different things with the outputted code blocks. For runtime mode, in Python/numpy code is executed by simply calling the `exec` statement on the code block in a given namespace. In standalone mode, the templates will typically each be saved into different files.

## Key concepts

### Namespaces

In general, a namespace is simply a mapping/dict from names to values. In Brian we use the term ‘namespace’ in two ways: the high level “abstract namespace” maps names to objects based on the `Variables` or [`Function`](../reference/brian2.core.functions.Function.html#brian2.core.functions.Function "brian2.core.functions.Function") class. In the above example, `v` maps to an `ArrayVariable` object, `tau` to a `Constant` object, etc. This namespace has all the information that is needed for checking the consistency of units, to determine which variables are boolean or scalar, etc. During the `CodeObject` creation, this abstract namespace is converted into the final namespace in which the code will be executed. In this namespace, `v` maps to the numpy array storing the state variable values (without units) and `tau` maps to a concrete value (again, without units). See [Equations and namespaces](equations_namespaces.html) for more details.

### Variable

`Variable` objects contain information about the variable they correspond to, including details like the data type, whether it is a single value or an array, etc.

See `brian2.core.variables` and, e.g. `Group._create_variables`, `NeuronGroup._create_variables`.

### Templates

Templates are stored in Jinja2 format. They come in one of two forms, either they are a single template if code generation only needs to output a single block of code, or they define multiple Jinja macros, each of which is a separate code block. The `CodeObject` should define what type of template it wants, and the names of the macros to define. For examples, see the templates in the directories in `brian2/codegen/runtime`. See `brian2.codegen.templates` for more details.

## Code guide

This section includes a guide to the various relevant packages and subpackages involved in the code generation process.

`codegen`
    

Stores the majority of all code generation related code.

`codegen.functions`
    

Code related to including functions - built-in and user-defined - in generated code.

`codegen.generators`
    

Each `CodeGenerator` is defined in a module here.

`codegen.runtime`
    

Each runtime `CodeObject` and its templates are defined in a package here.

`core`
    

`core.variables`
    

The `Variable` types are defined here.

`equations`
    

Everything related to [`Equations`](../reference/brian2.equations.equations.Equations.html#brian2.equations.equations.Equations "brian2.equations.equations.Equations").

`groups`
    

All [`Group`](../reference/brian2.groups.group.Group.html#brian2.groups.group.Group "brian2.groups.group.Group") related stuff is in here. The `Group.resolve` methods are responsible for determining the abstract namespace.

`parsing`
    

Various tools using Python’s `ast` module to parse user-specified code. Includes syntax translation to various languages in `parsing.rendering`.

`stateupdaters`
    

Everything related to generating abstract code blocks from integration methods is here.

---

# Physical units2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/user/units.html

# Physical units

  * Using units

  * Removing units

  * Temperatures

  * Constants

  * Importing units

  * In-place operations on quantities

Brian includes a system for physical units. The base units are defined by their standard SI unit names: `amp`/`ampere`, `kilogram`/`kilogramme`, `second`, `metre`/`meter`, `mole`/`mol`, `kelvin`, and `candela`. In addition to these base units, Brian defines a set of derived units: `coulomb`, `farad`, `gram`/`gramme`, `hertz`, `joule`, `liter`/ `litre`, `molar`, `pascal`, `ohm`, `siemens`, `volt`, `watt`, together with prefixed versions (e.g. `msiemens = 0.001*siemens`) using the prefixes `p, n, u, m, k, M, G, T` (two exceptions to this rule: `kilogram` is not defined with any additional prefixes, and `metre` and `meter` are additionaly defined with the “centi” prefix, i.e. `cmetre`/`cmeter`). For convenience, a couple of additional useful standard abbreviations such as `cm` (instead of `cmetre`/`cmeter`), `nS` (instead of `nsiemens`), `ms` (instead of `msecond`), `Hz` (instead of `hertz`), `mM` (instead of `mmolar`) are included. To avoid clashes with common variable names, no one-letter abbreviations are provided (e.g. you can use `mV` or `nS`, but _not_ `V` or `S`).

## Using units

You can generate a physical quantity by multiplying a scalar or vector value with its physical unit:
    
    
    >>> tau = 20*ms
    >>> print(tau)
    20. ms
    >>> rates = [10, 20, 30]*Hz
    >>> print(rates)
    [ 10.  20.  30.] Hz
    

Brian will check the consistency of operations on units and raise an error for dimensionality mismatches:
    
    
    >>> tau += 1  # ms? second?  
    Traceback (most recent call last):
    ...
    DimensionMismatchError: Cannot calculate ... += 1, units do not match (units are second and 1).
    >>> 3*kgram + 3*amp   
    Traceback (most recent call last):
    ...
    DimensionMismatchError: Cannot calculate 3. kg + 3. A, units do not match (units are kilogram and amp).
    

Most Brian functions will also complain about non-specified or incorrect units:
    
    
    >>> G = NeuronGroup(10, 'dv/dt = -v/tau: volt', dt=0.5)   
    Traceback (most recent call last):
    ...
    DimensionMismatchError: Function "__init__" expected a quantitity with unit second for argument "dt" but got 0.5 (unit is 1).
    

Numpy functions have been overwritten to correctly work with units (see the [developer documentation](../developer/units.html) for more details):
    
    
    >>> print(mean(rates))
    20. Hz
    >>> print(rates.repeat(2))
    [ 10.  10.  20.  20.  30.  30.] Hz
    

## Removing units

There are various options to remove the units from a value (e.g. to use it with analysis functions that do not correctly work with units)

  * Divide the value by its unit (most of the time the recommended option because it is clear about the scale)

  * Transform it to a pure numpy array in the base unit by calling [`asarray`](https://numpy.org/doc/stable/reference/generated/numpy.asarray.html#numpy.asarray "\(in NumPy v2.0\)") (no copy) or [`array`](https://numpy.org/doc/stable/reference/generated/numpy.array.html#numpy.array "\(in NumPy v2.0\)") (copy)

  * Directly get the unitless value of a state variable by appending an underscore to the name

    
    
    >>> tau/ms
    20.0
    >>> asarray(rates)
    array([ 10.,  20.,  30.])
    >>> G = NeuronGroup(5, 'dv/dt = -v/tau: volt')
    >>> print(G.v_[:])
    [ 0.  0.  0.  0.  0.]
    

## Temperatures

Brian only supports temperatures defined in °K, using the provided `kelvin` unit object. Other conventions such as °C, or °F are not compatible with Brian’s unit system, because they cannot be expressed as a multiplicative scaling of the SI base unit kelvin (their zero point is different). However, in biological experiments and modeling, temperatures are typically reported in °C. How to use such temperatures depends on whether they are used as _temperature differences_ or as _absolute temperatures_ :

temperature differences
    

Their major use case is the correction of time constants for differences in temperatures based on the [Q10 temperature coefficient](https://en.wikipedia.org/wiki/Q10_\(temperature_coefficient\)). In this case, all temperatures can directly use `kelvin` even though the temperatures are reported in Celsius, since temperature differences in Celsius and Kelvin are identical.

absolute temperatures
    

Equations such as the [Goldman–Hodgkin–Katz voltage equation](https://en.wikipedia.org/wiki/Goldman_equation) have a factor that depends on the absolute temperature measured in Kelvin. To get this temperature from a temperature reported in °C, you can use the `zero_celsius` constant from the [`brian2.units.constants`](../reference/brian2.units.html#module-brian2.units.constants "brian2.units.constants") package (see below):
    
    
    from brian2.units.constants import zero_celsius
    
    celsius_temp = 27
    abs_temp = celsius_temp*kelvin + zero_celsius
    

Note

Earlier versions of Brian had a `celsius` unit which was in fact identical to `kelvin`. While this gave the correct results for temperature differences, it did not correctly work for absolute temperatures. To avoid confusion and possible misinterpretation, the `celsius` unit has therefore been removed.

## Constants

The [`brian2.units.constants`](../reference/brian2.units.html#module-brian2.units.constants "brian2.units.constants") package provides a range of physical constants that can be useful for detailed biological models. Brian provides the following constants:

Constant | Symbol(s) | Brian name | Value  
---|---|---|---  
Avogadro constant | \\(N_A, L\\) | `avogadro_constant` | \\(6.022140857\times 10^{23}\,\mathrm{mol}^{-1}\\)  
Boltzmann constant | \\(k\\) | `boltzmann_constant` | \\(1.38064852\times 10^{-23}\,\mathrm{J}\,\mathrm{K}^{-1}\\)  
Electric constant | \\(\epsilon_0\\) | `electric_constant` | \\(8.854187817\times 10^{-12}\,\mathrm{F}\,\mathrm{m}^{-1}\\)  
Electron mass | \\(m_e\\) | `electron_mass` | \\(9.10938356\times 10^{-31}\,\mathrm{kg}\\)  
Elementary charge | \\(e\\) | `elementary_charge` | \\(1.6021766208\times 10^{-19}\,\mathrm{C}\\)  
Faraday constant | \\(F\\) | `faraday_constant` | \\(96485.33289\,\mathrm{C}\,\mathrm{mol}^{-1}\\)  
Gas constant | \\(R\\) | `gas_constant` | \\(8.3144598\,\mathrm{J}\,\mathrm{mol}^{-1}\,\mathrm{K}^{-1}\\)  
Magnetic constant | \\(\mu_0\\) | `magnetic_constant` | \\(12.566370614\times 10^{-7}\,\mathrm{N}\,\mathrm{A}^{-2}\\)  
Molar mass constant | \\(M_u\\) | `molar_mass_constant` | \\(1\times 10^{-3}\,\mathrm{kg}\,\mathrm{mol}^{-1}\\)  
0°C |  | `zero_celsius` | \\(273.15\,\mathrm{K}\\)  
  
Note that these constants are not imported by default, you will have to explicitly import them from [`brian2.units.constants`](../reference/brian2.units.html#module-brian2.units.constants "brian2.units.constants"). During the import, you can also give them shorter names using Python’s `from ... import ... as ...` syntax. For example, to calculate the \\(\frac{RT}{F}\\) factor that appears in the [Goldman–Hodgkin–Katz voltage equation](https://en.wikipedia.org/wiki/Goldman_equation) you can use:
    
    
    from brian2 import *
    from brian2.units.constants import zero_celsius, gas_constant as R, faraday_constant as F
    
    celsius_temp = 27
    T = celsius_temp*kelvin + zero_celsius
    factor = R*T/F
    

The following topics are not essential for beginners.

  

## Importing units

Brian generates standard names for units, combining the unit name (e.g. “siemens”) with a prefixes (e.g. “m”), and also generates squared and cubed versions by appending a number. For example, the units “msiemens”, “siemens2”, “usiemens3” are all predefined. You can import these units from the package `brian2.units.allunits` – accordingly, an `from brian2.units.allunits import *` will result in everything from `Ylumen3` (cubed yotta lumen) to `ymol` (yocto mole) being imported.

A better choice is normally to do `from brian2.units import *` or import everything `from brian2 import *` which only imports the units mentioned in the introductory paragraph (base units, derived units, and some standard abbreviations).

## In-place operations on quantities

In-place operations on quantity arrays change the underlying array, in the same way as for standard numpy arrays. This means, that any other variables referencing the same object will be affected as well:
    
    
    >>> q = [1, 2] * mV
    >>> r = q
    >>> q += 1*mV
    >>> q
    array([ 2.,  3.]) * mvolt
    >>> r
    array([ 2.,  3.]) * mvolt
    

In contrast, scalar quantities will never change the underlying value but instead return a new value (in the same way as standard Python scalars):
    
    
    >>> x = 1*mV
    >>> y = x
    >>> x *= 2
    >>> x
    2. * mvolt
    >>> y
    1. * mvolt
    

---

# Preferences system2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/developer/preferences.html

# Preferences system

Each preference looks like `codegen.c.compiler`, i.e. dotted names. Each preference has to be registered and validated. The idea is that registering all preferences ensures that misspellings of a preference value by a user causes an error, e.g. if they wrote `codgen.c.compiler` it would raise an error. Validation means that the value is checked for validity, so `codegen.c.compiler = 'gcc'` would be allowed, but `codegen.c.compiler = 'hcc'` would cause an error.

An additional requirement is that the preferences system allows for extension modules to define their own preferences, including extending the existing core brian preferences. For example, an extension might want to define `extension.*` but it might also want to define a new language for codegen, e.g. `codegen.lisp.*`. However, extensions cannot add preferences to an existing category.

## Accessing and setting preferences

Preferences can be accessed and set either keyword-based or attribute-based. To set/get the value for the preference example mentioned before, the following are equivalent:
    
    
    prefs['codegen.c.compiler'] = 'gcc'
    prefs.codegen.c.compiler = 'gcc'
    
    if prefs['codegen.c.compiler'] == 'gcc':
        ...
    if prefs.codegen.c.compiler == 'gcc':
        ...
    

Using the attribute-based form can be particulary useful for interactive work, e.g. in ipython, as it offers autocompletion and documentation. In ipython, `prefs.codegen.c?` would display a docstring with all the preferences available in the `codegen.c` category.

## Preference files

Preferences are stored in a hierarchy of files, with the following order (each step overrides the values in the previous step but no error is raised if one is missing):

  * The global defaults are stored in the installation directory.

  * The user default are stored in `~/.brian/preferences` (which works on Windows as well as Linux).

  * The file `brian_preferences` in the current directory.

## Registration

Registration of preferences is performed by a call to [`BrianGlobalPreferences.register_preferences`](../reference/brian2.core.preferences.BrianGlobalPreferences.html#brian2.core.preferences.BrianGlobalPreferences.register_preferences "brian2.core.preferences.BrianGlobalPreferences.register_preferences"), e.g.:
    
    
    register_preferences(
        'codegen.c',
        'Code generation preferences for the C language',
        'compiler'= BrianPreference(
            validator=is_compiler,
            docs='...',
            default='gcc'),
         ...
        )
    

The first argument `'codegen.c'` is the base name, and every preference of the form `codegen.c.*` has to be registered by this function (preferences in subcategories such as `codegen.c.somethingelse.*` have to be specified separately). In other words, by calling [`register_preferences`](../reference/brian2.core.preferences.BrianGlobalPreferences.html#brian2.core.preferences.BrianGlobalPreferences.register_preferences "brian2.core.preferences.BrianGlobalPreferences.register_preferences"), a module takes ownership of all the preferences with one particular base name. The second argument is a descriptive text explaining what this category is about. The preferences themselves are provided as keyword arguments, each set to a [`BrianPreference`](../reference/brian2.core.preferences.BrianPreference.html#brian2.core.preferences.BrianPreference "brian2.core.preferences.BrianPreference") object.

## Validation functions

A validation function takes a value for the preference and returns `True` (if the value is a valid value) or `False`. If no validation function is specified, a default validator is used that compares the value against the default value: Both should belong to the same class (e.g. int or str) and, in the case of a [`Quantity`](../reference/brian2.units.fundamentalunits.Quantity.html#brian2.units.fundamentalunits.Quantity "brian2.units.fundamentalunits.Quantity") have the same unit.

## Validation

Setting the value of a preference with a registered base name instantly triggers validation. Trying to set an unregistered preference using keyword or attribute access raises an error. The only exception from this rule is when the preferences are read from configuration files (see below). Since this happens before the user has the chance to import extensions that potentially define new preferences, this uses a special function (`_set_preference`). In this case,for base names that are not yet registered, validation occurs when the base name is registered. If, at the time that [`Network.run`](../reference/brian2.core.network.Network.html#brian2.core.network.Network.run "brian2.core.network.Network.run") is called, there are unregistered preferences set, a [`PreferenceError`](../reference/brian2.core.preferences.PreferenceError.html#brian2.core.preferences.PreferenceError "brian2.core.preferences.PreferenceError") is raised.

## File format

The preference files are of the following form:
    
    
    a.b.c = 1
    # Comment line
    [a]
    b.d = 2
    [a.b]
    b.e = 3
    

This would set preferences `a.b.c=1`, `a.b.d=2` and `a.b.e=3`.

## Built-in preferences

Brian itself defines the following preferences:

### GSL

Directory containing GSL code

`GSL.directory` = `None`
    

Set path to directory containing GSL header files (gsl_odeiv2.h etc.) If this directory is already in Python’s include (e.g. because of conda installation), this path can be set to None.

### codegen

Code generation preferences

`codegen.loop_invariant_optimisations` = `True`

> Whether to pull out scalar expressions out of the statements, so that they are only evaluated once instead of once for every neuron/synapse/… Can be switched off, e.g. because it complicates the code (and the same optimisation is already performed by the compiler) or because the code generation target does not deal well with it. Defaults to `True`.

`codegen.max_cache_dir_size` = `1000`

> The size of a directory (in MB) with cached code for Cython that triggers a warning. Set to 0 to never get a warning.

`codegen.string_expression_target` = `'numpy'`

> Default target for the evaluation of string expressions (e.g. when indexing state variables). Should normally not be changed from the default numpy target, because the overhead of compiling code is not worth the speed gain for simple expressions.
> 
> Accepts the same arguments as [codegen.target](../reference/brian2.codegen.html#brian-pref-codegen-target), except for `'auto'`

`codegen.target` = `'auto'`

> Default target for code generation.
> 
> Can be a string, in which case it should be one of:
> 
>   * `'auto'` the default, automatically chose the best code generation target available.
> 
>   * `'cython'`, uses the Cython package to generate C++ code. Needs a working installation of Cython and a C++ compiler.
> 
>   * `'numpy'` works on all platforms and doesn’t need a C compiler but is often less efficient.
> 
> 

> 
> Or it can be a `CodeObject` class.

**codegen.cpp**

C++ compilation preferences

`codegen.cpp.compiler` = `''`

> Compiler to use (uses default if empty). Should be `'unix'` or `'msvc'`.
> 
> To specify a specific compiler binary on unix systems, set the `CXX` environment variable instead.

`codegen.cpp.define_macros` = `[]`

> List of macros to define; each macro is defined using a 2-tuple, where ‘value’ is either the string to define it to or None to define it without a particular value (equivalent of “#define FOO” in source or -DFOO on Unix C compiler command line).

`codegen.cpp.extra_compile_args` = `None`

> Extra arguments to pass to compiler (if None, use either `extra_compile_args_gcc` or `extra_compile_args_msvc`).

`codegen.cpp.extra_compile_args_gcc` = `['-w', '-O3', '-ffast-math', '-fno-finite-math-only', '-march=native', '-std=c++11']`

> Extra compile arguments to pass to GCC compiler

`codegen.cpp.extra_compile_args_msvc` = `['/Ox', '/w', '', '/MP']`

> Extra compile arguments to pass to MSVC compiler (the default `/arch:` flag is determined based on the processor architecture)

`codegen.cpp.extra_link_args` = `[]`

> Any extra platform- and compiler-specific information to use when linking object files together.

`codegen.cpp.headers` = `[]`

> A list of strings specifying header files to use when compiling the code. The list might look like [“<vector>”,“‘my_header’”]. Note that the header strings need to be in a form than can be pasted at the end of a #include statement in the C++ code.

`codegen.cpp.include_dirs` = `['/path/to/your/Python/environment/include']`

> Include directories to use. The default value is `$prefix/include` (or `$prefix/Library/include` on Windows), where `$prefix` is Python’s site-specific directory prefix as returned by [`sys.prefix`](https://docs.python.org/3/library/sys.html#sys.prefix "\(in Python v3.12\)"). This will make compilation use library files installed into a conda environment.

`codegen.cpp.libraries` = `[]`

> List of library names (not filenames or paths) to link against.

`codegen.cpp.library_dirs` = `['/path/to/your/Python/environment/lib']`

> List of directories to search for C/C++ libraries at link time. The default value is `$prefix/lib` (or `$prefix/Library/lib` on Windows), where `$prefix` is Python’s site-specific directory prefix as returned by [`sys.prefix`](https://docs.python.org/3/library/sys.html#sys.prefix "\(in Python v3.12\)"). This will make compilation use library files installed into a conda environment.

`codegen.cpp.msvc_architecture` = `''`

> MSVC architecture name (or use system architectue by default).
> 
> Could take values such as x86, amd64, etc.

`codegen.cpp.msvc_vars_location` = `''`

> Location of the MSVC command line tool (or search for best by default).

`codegen.cpp.runtime_library_dirs` = `['/path/to/your/Python/environment/lib']`

> List of directories to search for C/C++ libraries at run time. The default value is `$prefix/lib` (not used on Windows), where `$prefix` is Python’s site-specific directory prefix as returned by [`sys.prefix`](https://docs.python.org/3/library/sys.html#sys.prefix "\(in Python v3.12\)"). This will make compilation use library files installed into a conda environment.

**codegen.generators**

Codegen generator preferences (see subcategories for individual languages)

**codegen.generators.cpp**

C++ codegen preferences

`codegen.generators.cpp.flush_denormals` = `False`

> Adds code to flush denormals to zero.
> 
> The code is gcc and architecture specific, so may not compile on all platforms. The code, for reference is:
>     
>     
>     #define CSR_FLUSH_TO_ZERO         (1 << 15)
>     unsigned csr = __builtin_ia32_stmxcsr();
>     csr |= CSR_FLUSH_TO_ZERO;
>     __builtin_ia32_ldmxcsr(csr);
>     
> 
> Found at <http://stackoverflow.com/questions/2487653/avoiding-denormal-values-in-c>.

`codegen.generators.cpp.restrict_keyword` = `'__restrict'`

> The keyword used for the given compiler to declare pointers as restricted.
> 
> This keyword is different on different compilers, the default works for gcc and MSVS.

**codegen.runtime**

Runtime codegen preferences (see subcategories for individual targets)

**codegen.runtime.cython**

Cython runtime codegen preferences

`codegen.runtime.cython.cache_dir` = `None`

> Location of the cache directory for Cython files. By default, will be stored in a `brian_extensions` subdirectory where Cython inline stores its temporary files (the result of `get_cython_cache_dir()`).

`codegen.runtime.cython.delete_source_files` = `True`

> Whether to delete source files after compiling. The Cython source files can take a significant amount of disk space, and are not used anymore when the compiled library file exists. They are therefore deleted by default, but keeping them around can be useful for debugging.

`codegen.runtime.cython.multiprocess_safe` = `True`

> Whether to use a lock file to prevent simultaneous write access to cython .pyx and .so files.

**codegen.runtime.numpy**

Numpy runtime codegen preferences

`codegen.runtime.numpy.discard_units` = `False`

> Whether to change the namespace of user-specifed functions to remove units.

### core

Core Brian preferences

`core.default_float_dtype` = `float64`

> Default dtype for all arrays of scalars (state variables, weights, etc.).

`core.default_integer_dtype` = `int32`

> Default dtype for all arrays of integer scalars.

`core.outdated_dependency_error` = `True`

> Whether to raise an error for outdated dependencies (`True`) or just a warning (`False`).

**core.network**

Network preferences

`core.network.default_schedule` = `['start', 'groups', 'thresholds', 'synapses', 'resets', 'end']`

> Default schedule used for networks that don’t specify a schedule.

### devices

Device preferences

**devices.cpp_standalone**

C++ standalone preferences

`devices.cpp_standalone.extra_make_args_unix` = `['-j']`

> Additional flags to pass to the GNU make command on Linux/OS-X. Defaults to “-j” for parallel compilation.

`devices.cpp_standalone.extra_make_args_windows` = `[]`

> Additional flags to pass to the nmake command on Windows. By default, no additional flags are passed.

`devices.cpp_standalone.make_cmd_unix` = `'make'`

> The make command used to compile the standalone project. Defaults to the standard GNU make commane “make”.

`devices.cpp_standalone.openmp_spatialneuron_strategy` = `None`

> DEPRECATED. Previously used to chose the strategy to parallelize the solution of the three tridiagonal systems for multicompartmental neurons. Now, its value is ignored.

`devices.cpp_standalone.openmp_threads` = `0`

> The number of threads to use if OpenMP is turned on. By default, this value is set to 0 and the C++ code is generated without any reference to OpenMP. If greater than 0, then the corresponding number of threads are used to launch the simulation.

`devices.cpp_standalone.run_cmd_unix` = `'./main'`

> The command used to run the compiled standalone project. Defaults to executing the compiled binary with “./main”. Must be a single binary as string or a list of command arguments (e.g. [“./binary”, “–key”, “value”]).

`devices.cpp_standalone.run_environment_variables` = `{'LD_BIND_NOW': '1'}`

> Dictionary of environment variables and their values that will be set during the execution of the standalone code.

### legacy

Preferences to enable legacy behaviour

`legacy.refractory_timing` = `False`

> Whether to use the semantics for checking the refractoriness condition that were in place up until (including) version 2.1.2. In that implementation, refractory periods that were multiples of dt could lead to a varying number of refractory timesteps due to the nature of floating point comparisons). This preference is only provided for exact reproducibility of previously obtained results, new simulations should use the improved mechanism which uses a more robust mechanism to convert refractoriness into timesteps. Defaults to `False`.

### logging

Logging system preferences

`logging.console_log_level` = `'INFO'`

> What log level to use for the log written to the console.
> 
> Has to be one of CRITICAL, ERROR, WARNING, INFO, DEBUG or DIAGNOSTIC.

`logging.delete_log_on_exit` = `True`

> Whether to delete the log and script file on exit.
> 
> If set to `True` (the default), log files (and the copy of the main script) will be deleted after the brian process has exited, unless an uncaught exception occurred. If set to `False`, all log files will be kept.

`logging.display_brian_error_message` = `True`

> Whether to display a text for uncaught errors, mentioning the location of the log file, the mailing list and the github issues.
> 
> Defaults to `True`.

`logging.file_log` = `True`

> Whether to log to a file or not.
> 
> If set to `True` (the default), logging information will be written to a file. The log level can be set via the [logging.file_log_level](../reference/brian2.utils.html#brian-pref-logging-file-log-level) preference.

`logging.file_log_level` = `'DEBUG'`

> What log level to use for the log written to the log file.
> 
> In case file logging is activated (see [logging.file_log](../reference/brian2.utils.html#brian-pref-logging-file-log)), which log level should be used for logging. Has to be one of CRITICAL, ERROR, WARNING, INFO, DEBUG or DIAGNOSTIC.

`logging.file_log_max_size` = `10000000`

> The maximum size for the debug log before it will be rotated.
> 
> If set to any value `> 0`, the debug log will be rotated once this size is reached. Rotating the log means that the old debug log will be moved into a file in the same directory but with suffix `".1"` and the a new log file will be created with the same pathname as the original file. Only one backup is kept; if a file with suffix `".1"` already exists when rotating, it will be overwritten. If set to `0`, no log rotation will be applied. The default setting rotates the log file after 10MB.

`logging.save_script` = `True`

> Whether to save a copy of the script that is run.
> 
> If set to `True` (the default), a copy of the currently run script is saved to a temporary location. It is deleted after a successful run (unless [logging.delete_log_on_exit](../reference/brian2.utils.html#brian-pref-logging-delete-log-on-exit) is `False`) but is kept after an uncaught exception occured. This can be helpful for debugging, in particular when several simulations are running in parallel.

`logging.std_redirection` = `True`

> Whether or not to redirect stdout/stderr to null at certain places.
> 
> This silences a lot of annoying compiler output, but will also hide error messages making it harder to debug problems. You can always temporarily switch it off when debugging. If [logging.std_redirection_to_file](../reference/brian2.utils.html#brian-pref-logging-std-redirection-to-file) is set to `True` as well, then the output is saved to a file and if an error occurs the name of this file will be printed.

`logging.std_redirection_to_file` = `True`

> Whether to redirect stdout/stderr to a file.
> 
> If both `logging.std_redirection` and this preference are set to `True`, all standard output/error (most importantly output from the compiler) will be stored in files and if an error occurs the name of this file will be printed. If [logging.std_redirection](../reference/brian2.utils.html#brian-pref-logging-std-redirection) is `True` and this preference is `False`, then all standard output/error will be completely suppressed, i.e. neither be displayed nor stored in a file.
> 
> The value of this preference is ignore if [logging.std_redirection](../reference/brian2.utils.html#brian-pref-logging-std-redirection) is set to `False`.

---

# Preferences2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/advanced/preferences.html

# Preferences

Brian has a system of global preferences that affect how certain objects behave. These can be set either in scripts by using the [`prefs`](../reference/brian2.core.preferences.prefs.html#brian2.core.preferences.prefs "brian2.core.preferences.prefs") object or in a file. Each preference looks like `codegen.cpp.compiler`, i.e. dotted names.

## Accessing and setting preferences

Preferences can be accessed and set either keyword-based or attribute-based. The following are equivalent:
    
    
    prefs['codegen.cpp.compiler'] = 'unix'
    prefs.codegen.cpp.compiler = 'unix'
    

Using the attribute-based form can be particulary useful for interactive work, e.g. in ipython, as it offers autocompletion and documentation. In ipython, `prefs.codegen.cpp?` would display a docstring with all the preferences available in the `codegen.cpp` category.

## Preference files

Preferences are stored in a hierarchy of files, with the following order (each step overrides the values in the previous step but no error is raised if one is missing):

  * The user default are stored in `~/.brian/user_preferences` (which works on Windows as well as Linux). The `~` symbol refers to the user directory.

  * The file `brian_preferences` in the current directory.

The preference files are of the following form:
    
    
    a.b.c = 1
    # Comment line
    [a]
    b.d = 2
    [a.b]
    b.e = 3
    

This would set preferences `a.b.c=1`, `a.b.d=2` and `a.b.e=3`.

File setting all preferences to their default values
    
    
    #-------------------------------------------------------------------------------
    # Logging system preferences
    #-------------------------------------------------------------------------------
    
    [logging]
    
    # What log level to use for the log written to the console.
    # 
    # Has to be one of CRITICAL, ERROR, WARNING, INFO, DEBUG or DIAGNOSTIC.
    
    console_log_level = 'INFO'
    
    # Whether to delete the log and script file on exit.
    # 
    # If set to ``True`` (the default), log files (and the copy of the main
    # script) will be deleted after the brian process has exited, unless an
    # uncaught exception occurred. If set to ``False``, all log files will be
    # kept.
    
    delete_log_on_exit = True
    
    # Whether to display a text for uncaught errors, mentioning the location
    # of the log file, the mailing list and the github issues.
    # 
    # Defaults to ``True``.
    
    display_brian_error_message = True
    
    # Whether to log to a file or not.
    # 
    # If set to ``True`` (the default), logging information will be written
    # to a file. The log level can be set via the `logging.file_log_level`
    # preference.
    
    file_log = True
    
    # What log level to use for the log written to the log file.
    # 
    # In case file logging is activated (see `logging.file_log`), which log
    # level should be used for logging. Has to be one of CRITICAL, ERROR,
    # WARNING, INFO, DEBUG or DIAGNOSTIC.
    
    file_log_level = 'DEBUG'
    
    # The maximum size for the debug log before it will be rotated.
    # 
    # If set to any value ``> 0``, the debug log will be rotated once
    # this size is reached. Rotating the log means that the old debug log
    # will be moved into a file in the same directory but with suffix ``".1"``
    # and the a new log file will be created with the same pathname as the
    # original file. Only one backup is kept; if a file with suffix ``".1"``
    # already exists when rotating, it will be overwritten.
    # If set to ``0``, no log rotation will be applied.
    # The default setting rotates the log file after 10MB.
    
    file_log_max_size = 10000000
    
    # Whether to save a copy of the script that is run.
    # 
    # If set to ``True`` (the default), a copy of the currently run script
    # is saved to a temporary location. It is deleted after a successful
    # run (unless `logging.delete_log_on_exit` is ``False``) but is kept after
    # an uncaught exception occured. This can be helpful for debugging,
    # in particular when several simulations are running in parallel.
    
    save_script = True
    
    # Whether or not to redirect stdout/stderr to null at certain places.
    # 
    # This silences a lot of annoying compiler output, but will also hide
    # error messages making it harder to debug problems. You can always
    # temporarily switch it off when debugging. If
    # `logging.std_redirection_to_file` is set to ``True`` as well, then the
    # output is saved to a file and if an error occurs the name of this file
    # will be printed.
    
    std_redirection = True
    
    # Whether to redirect stdout/stderr to a file.
    # 
    # If both ``logging.std_redirection`` and this preference are set to
    # ``True``, all standard output/error (most importantly output from
    # the compiler) will be stored in files and if an error occurs the name
    # of this file will be printed. If `logging.std_redirection` is ``True``
    # and this preference is ``False``, then all standard output/error will
    # be completely suppressed, i.e. neither be displayed nor stored in a
    # file.
    # 
    # The value of this preference is ignore if `logging.std_redirection` is
    # set to ``False``.
    
    std_redirection_to_file = True
    
    #-------------------------------------------------------------------------------
    # Runtime codegen preferences (see subcategories for individual targets)
    #-------------------------------------------------------------------------------
    
    [codegen.runtime]
    
    #-------------------------------------------------------------------------------
    # Codegen generator preferences (see subcategories for individual languages)
    #-------------------------------------------------------------------------------
    
    [codegen.generators]
    
    #-------------------------------------------------------------------------------
    # C++ compilation preferences
    #-------------------------------------------------------------------------------
    
    [codegen.cpp]
    
    # Compiler to use (uses default if empty).
    # Should be ``'unix'`` or ``'msvc'``.
    # 
    # To specify a specific compiler binary on unix systems, set the `CXX` environment
    # variable instead.
    
    compiler = ''
    
    # List of macros to define; each macro is defined using a 2-tuple,
    # where 'value' is either the string to define it to or None to
    # define it without a particular value (equivalent of "#define
    # FOO" in source or -DFOO on Unix C compiler command line).
    
    define_macros = []
    
    # Extra arguments to pass to compiler (if None, use either
    # ``extra_compile_args_gcc`` or ``extra_compile_args_msvc``).
    
    extra_compile_args = None
    
    # Extra compile arguments to pass to GCC compiler
    
    extra_compile_args_gcc = ['-w', '-O3', '-ffast-math', '-fno-finite-math-only', '-march=native', '-std=c++11']
    
    # Extra compile arguments to pass to MSVC compiler (the default
    # ``/arch:`` flag is determined based on the processor architecture)
    
    extra_compile_args_msvc = ['/Ox', '/w', '', '/MP']
    
    # Any extra platform- and compiler-specific information to use when
    # linking object files together.
    
    extra_link_args = []
    
    # A list of strings specifying header files to use when compiling the
    # code. The list might look like ["<vector>","'my_header'"]. Note that
    # the header strings need to be in a form than can be pasted at the end
    # of a #include statement in the C++ code.
    
    headers = []
    
    # Include directories to use.
    # The default value is ``$prefix/include`` (or ``$prefix/Library/include``
    # on Windows), where ``$prefix`` is Python's site-specific directory
    # prefix as returned by `sys.prefix`. This will make compilation use
    # library files installed into a conda environment.
    
    include_dirs = ['/path/to/your/Python/environment/include']
    
    # List of library names (not filenames or paths) to link against.
    
    libraries = []
    
    # List of directories to search for C/C++ libraries at link time.
    # The default value is ``$prefix/lib`` (or ``$prefix/Library/lib``
    # on Windows), where ``$prefix`` is Python's site-specific directory
    # prefix as returned by `sys.prefix`. This will make compilation use
    # library files installed into a conda environment.
    
    library_dirs = ['/path/to/your/Python/environment/lib']
    
    # MSVC architecture name (or use system architectue by default).
    # 
    # Could take values such as x86, amd64, etc.
    
    msvc_architecture = ''
    
    # Location of the MSVC command line tool (or search for best by default).
    
    msvc_vars_location = ''
    
    # List of directories to search for C/C++ libraries at run time.
    # The default value is ``$prefix/lib`` (not used on Windows), where
    # ``$prefix`` is Python's site-specific directory prefix as returned by
    # `sys.prefix`. This will make compilation use library files installed
    # into a conda environment.
    
    runtime_library_dirs = ['/path/to/your/Python/environment/lib']
    
    #-------------------------------------------------------------------------------
    # C++ codegen preferences
    #-------------------------------------------------------------------------------
    
    [codegen.generators.cpp]
    
    # Adds code to flush denormals to zero.
    # 
    # The code is gcc and architecture specific, so may not compile on all
    # platforms. The code, for reference is::
    # 
    #     #define CSR_FLUSH_TO_ZERO         (1 << 15)
    #     unsigned csr = __builtin_ia32_stmxcsr();
    #     csr |= CSR_FLUSH_TO_ZERO;
    #     __builtin_ia32_ldmxcsr(csr);
    # 
    # Found at `<http://stackoverflow.com/questions/2487653/avoiding-denormal-values-in-c>`_.
    
    flush_denormals = False
    
    # The keyword used for the given compiler to declare pointers as restricted.
    # 
    # This keyword is different on different compilers, the default works for
    # gcc and MSVS.
    
    restrict_keyword = '__restrict'
    
    #-------------------------------------------------------------------------------
    # Device preferences
    #-------------------------------------------------------------------------------
    
    [devices]
    
    #-------------------------------------------------------------------------------
    # Directory containing GSL code
    #-------------------------------------------------------------------------------
    
    [GSL]
    
    # Set path to directory containing GSL header files (gsl_odeiv2.h etc.)
    # If this directory is already in Python's include (e.g. because of conda installation), this path can be set to None.
    
    directory = None
    
    #-------------------------------------------------------------------------------
    # Numpy runtime codegen preferences
    #-------------------------------------------------------------------------------
    
    [codegen.runtime.numpy]
    
    # Whether to change the namespace of user-specifed functions to remove
    # units.
    
    discard_units = False
    
    #-------------------------------------------------------------------------------
    # Cython runtime codegen preferences
    #-------------------------------------------------------------------------------
    
    [codegen.runtime.cython]
    
    # Location of the cache directory for Cython files. By default,
    # will be stored in a ``brian_extensions`` subdirectory
    # where Cython inline stores its temporary files
    # (the result of ``get_cython_cache_dir()``).
    
    cache_dir = None
    
    # Whether to delete source files after compiling. The Cython
    # source files can take a significant amount of disk space, and
    # are not used anymore when the compiled library file exists.
    # They are therefore deleted by default, but keeping them around
    # can be useful for debugging.
    
    delete_source_files = True
    
    # Whether to use a lock file to prevent simultaneous write access
    # to cython .pyx and .so files.
    
    multiprocess_safe = True
    
    #-------------------------------------------------------------------------------
    # Code generation preferences
    #-------------------------------------------------------------------------------
    
    [codegen]
    
    # Whether to pull out scalar expressions out of the statements, so that
    # they are only evaluated once instead of once for every neuron/synapse/...
    # Can be switched off, e.g. because it complicates the code (and the same
    # optimisation is already performed by the compiler) or because the
    # code generation target does not deal well with it. Defaults to ``True``.
    
    loop_invariant_optimisations = True
    
    # The size of a directory (in MB) with cached code for Cython that triggers
    # a warning. Set to 0 to never get a warning.
    
    max_cache_dir_size = 1000
    
    # Default target for the evaluation of string expressions (e.g. when
    # indexing state variables). Should normally not be changed from the
    # default numpy target, because the overhead of compiling code is not
    # worth the speed gain for simple expressions.
    # 
    # Accepts the same arguments as `codegen.target`, except for ``'auto'``
    
    string_expression_target = 'numpy'
    
    # Default target for code generation.
    # 
    # Can be a string, in which case it should be one of:
    # 
    # * ``'auto'`` the default, automatically chose the best code generation
    #   target available.
    # * ``'cython'``, uses the Cython package to generate C++ code. Needs a
    #   working installation of Cython and a C++ compiler.
    # * ``'numpy'`` works on all platforms and doesn't need a C compiler but
    #   is often less efficient.
    # 
    # Or it can be a ``CodeObject`` class.
    
    target = 'auto'
    
    #-------------------------------------------------------------------------------
    # Network preferences
    #-------------------------------------------------------------------------------
    
    [core.network]
    
    # Default schedule used for networks that
    # don't specify a schedule.
    
    default_schedule = ['start', 'groups', 'thresholds', 'synapses', 'resets', 'end']
    
    #-------------------------------------------------------------------------------
    # C++ standalone preferences
    #-------------------------------------------------------------------------------
    
    [devices.cpp_standalone]
    
    # Additional flags to pass to the GNU make command on Linux/OS-X.
    # Defaults to "-j" for parallel compilation.
    
    extra_make_args_unix = ['-j']
    
    # Additional flags to pass to the nmake command on Windows. By default, no
    # additional flags are passed.
    
    extra_make_args_windows = []
    
    # The make command used to compile the standalone project. Defaults to the
    # standard GNU make commane "make".
    
    make_cmd_unix = 'make'
    
    # DEPRECATED. Previously used to chose the strategy to parallelize the
    # solution of the three tridiagonal systems for multicompartmental
    # neurons. Now, its value is ignored.
    
    openmp_spatialneuron_strategy = None
    
    # The number of threads to use if OpenMP is turned on. By default, this value is set to 0 and the C++ code
    # is generated without any reference to OpenMP. If greater than 0, then the corresponding number of threads
    # are used to launch the simulation.
    
    openmp_threads = 0
    
    # The command used to run the compiled standalone project. Defaults to executing
    # the compiled binary with "./main". Must be a single binary as string or a list
    # of command arguments (e.g. ["./binary", "--key", "value"]).
    
    run_cmd_unix = './main'
    
    # Dictionary of environment variables and their values that will be set
    # during the execution of the standalone code.
    
    run_environment_variables = {'LD_BIND_NOW': '1'}
    
    #-------------------------------------------------------------------------------
    # Core Brian preferences
    #-------------------------------------------------------------------------------
    
    [core]
    
    # Default dtype for all arrays of scalars (state variables, weights, etc.).
    
    default_float_dtype = float64
    
    # Default dtype for all arrays of integer scalars.
    
    default_integer_dtype = int32
    
    # Whether to raise an error for outdated dependencies (``True``) or just
    # a warning (``False``).
    
    outdated_dependency_error = True
    
    #-------------------------------------------------------------------------------
    # Preferences to enable legacy behaviour
    #-------------------------------------------------------------------------------
    
    [legacy]
    
    # Whether to use the semantics for checking the refractoriness condition
    # that were in place up until (including) version 2.1.2. In that
    # implementation, refractory periods that were multiples of dt could lead
    # to a varying number of refractory timesteps due to the nature of
    # floating point comparisons). This preference is only provided for exact
    # reproducibility of previously obtained results, new simulations should
    # use the improved mechanism which uses a more robust mechanism to
    # convert refractoriness into timesteps. Defaults to ``False``.
    
    refractory_timing = False
    
    

## List of preferences

Brian itself defines the following preferences (including their default values):

### GSL

Directory containing GSL code

`GSL.directory` = `None`
    

Set path to directory containing GSL header files (gsl_odeiv2.h etc.) If this directory is already in Python’s include (e.g. because of conda installation), this path can be set to None.

### codegen

Code generation preferences

`codegen.loop_invariant_optimisations` = `True`

> Whether to pull out scalar expressions out of the statements, so that they are only evaluated once instead of once for every neuron/synapse/… Can be switched off, e.g. because it complicates the code (and the same optimisation is already performed by the compiler) or because the code generation target does not deal well with it. Defaults to `True`.

`codegen.max_cache_dir_size` = `1000`

> The size of a directory (in MB) with cached code for Cython that triggers a warning. Set to 0 to never get a warning.

`codegen.string_expression_target` = `'numpy'`

> Default target for the evaluation of string expressions (e.g. when indexing state variables). Should normally not be changed from the default numpy target, because the overhead of compiling code is not worth the speed gain for simple expressions.
> 
> Accepts the same arguments as [codegen.target](../reference/brian2.codegen.html#brian-pref-codegen-target), except for `'auto'`

`codegen.target` = `'auto'`

> Default target for code generation.
> 
> Can be a string, in which case it should be one of:
> 
>   * `'auto'` the default, automatically chose the best code generation target available.
> 
>   * `'cython'`, uses the Cython package to generate C++ code. Needs a working installation of Cython and a C++ compiler.
> 
>   * `'numpy'` works on all platforms and doesn’t need a C compiler but is often less efficient.
> 
> 

> 
> Or it can be a `CodeObject` class.

**codegen.cpp**

C++ compilation preferences

`codegen.cpp.compiler` = `''`

> Compiler to use (uses default if empty). Should be `'unix'` or `'msvc'`.
> 
> To specify a specific compiler binary on unix systems, set the `CXX` environment variable instead.

`codegen.cpp.define_macros` = `[]`

> List of macros to define; each macro is defined using a 2-tuple, where ‘value’ is either the string to define it to or None to define it without a particular value (equivalent of “#define FOO” in source or -DFOO on Unix C compiler command line).

`codegen.cpp.extra_compile_args` = `None`

> Extra arguments to pass to compiler (if None, use either `extra_compile_args_gcc` or `extra_compile_args_msvc`).

`codegen.cpp.extra_compile_args_gcc` = `['-w', '-O3', '-ffast-math', '-fno-finite-math-only', '-march=native', '-std=c++11']`

> Extra compile arguments to pass to GCC compiler

`codegen.cpp.extra_compile_args_msvc` = `['/Ox', '/w', '', '/MP']`

> Extra compile arguments to pass to MSVC compiler (the default `/arch:` flag is determined based on the processor architecture)

`codegen.cpp.extra_link_args` = `[]`

> Any extra platform- and compiler-specific information to use when linking object files together.

`codegen.cpp.headers` = `[]`

> A list of strings specifying header files to use when compiling the code. The list might look like [“<vector>”,“‘my_header’”]. Note that the header strings need to be in a form than can be pasted at the end of a #include statement in the C++ code.

`codegen.cpp.include_dirs` = `['/path/to/your/Python/environment/include']`

> Include directories to use. The default value is `$prefix/include` (or `$prefix/Library/include` on Windows), where `$prefix` is Python’s site-specific directory prefix as returned by [`sys.prefix`](https://docs.python.org/3/library/sys.html#sys.prefix "\(in Python v3.12\)"). This will make compilation use library files installed into a conda environment.

`codegen.cpp.libraries` = `[]`

> List of library names (not filenames or paths) to link against.

`codegen.cpp.library_dirs` = `['/path/to/your/Python/environment/lib']`

> List of directories to search for C/C++ libraries at link time. The default value is `$prefix/lib` (or `$prefix/Library/lib` on Windows), where `$prefix` is Python’s site-specific directory prefix as returned by [`sys.prefix`](https://docs.python.org/3/library/sys.html#sys.prefix "\(in Python v3.12\)"). This will make compilation use library files installed into a conda environment.

`codegen.cpp.msvc_architecture` = `''`

> MSVC architecture name (or use system architectue by default).
> 
> Could take values such as x86, amd64, etc.

`codegen.cpp.msvc_vars_location` = `''`

> Location of the MSVC command line tool (or search for best by default).

`codegen.cpp.runtime_library_dirs` = `['/path/to/your/Python/environment/lib']`

> List of directories to search for C/C++ libraries at run time. The default value is `$prefix/lib` (not used on Windows), where `$prefix` is Python’s site-specific directory prefix as returned by [`sys.prefix`](https://docs.python.org/3/library/sys.html#sys.prefix "\(in Python v3.12\)"). This will make compilation use library files installed into a conda environment.

**codegen.generators**

Codegen generator preferences (see subcategories for individual languages)

**codegen.generators.cpp**

C++ codegen preferences

`codegen.generators.cpp.flush_denormals` = `False`

> Adds code to flush denormals to zero.
> 
> The code is gcc and architecture specific, so may not compile on all platforms. The code, for reference is:
>     
>     
>     #define CSR_FLUSH_TO_ZERO         (1 << 15)
>     unsigned csr = __builtin_ia32_stmxcsr();
>     csr |= CSR_FLUSH_TO_ZERO;
>     __builtin_ia32_ldmxcsr(csr);
>     
> 
> Found at <http://stackoverflow.com/questions/2487653/avoiding-denormal-values-in-c>.

`codegen.generators.cpp.restrict_keyword` = `'__restrict'`

> The keyword used for the given compiler to declare pointers as restricted.
> 
> This keyword is different on different compilers, the default works for gcc and MSVS.

**codegen.runtime**

Runtime codegen preferences (see subcategories for individual targets)

**codegen.runtime.cython**

Cython runtime codegen preferences

`codegen.runtime.cython.cache_dir` = `None`

> Location of the cache directory for Cython files. By default, will be stored in a `brian_extensions` subdirectory where Cython inline stores its temporary files (the result of `get_cython_cache_dir()`).

`codegen.runtime.cython.delete_source_files` = `True`

> Whether to delete source files after compiling. The Cython source files can take a significant amount of disk space, and are not used anymore when the compiled library file exists. They are therefore deleted by default, but keeping them around can be useful for debugging.

`codegen.runtime.cython.multiprocess_safe` = `True`

> Whether to use a lock file to prevent simultaneous write access to cython .pyx and .so files.

**codegen.runtime.numpy**

Numpy runtime codegen preferences

`codegen.runtime.numpy.discard_units` = `False`

> Whether to change the namespace of user-specifed functions to remove units.

### core

Core Brian preferences

`core.default_float_dtype` = `float64`

> Default dtype for all arrays of scalars (state variables, weights, etc.).

`core.default_integer_dtype` = `int32`

> Default dtype for all arrays of integer scalars.

`core.outdated_dependency_error` = `True`

> Whether to raise an error for outdated dependencies (`True`) or just a warning (`False`).

**core.network**

Network preferences

`core.network.default_schedule` = `['start', 'groups', 'thresholds', 'synapses', 'resets', 'end']`

> Default schedule used for networks that don’t specify a schedule.

### devices

Device preferences

**devices.cpp_standalone**

C++ standalone preferences

`devices.cpp_standalone.extra_make_args_unix` = `['-j']`

> Additional flags to pass to the GNU make command on Linux/OS-X. Defaults to “-j” for parallel compilation.

`devices.cpp_standalone.extra_make_args_windows` = `[]`

> Additional flags to pass to the nmake command on Windows. By default, no additional flags are passed.

`devices.cpp_standalone.make_cmd_unix` = `'make'`

> The make command used to compile the standalone project. Defaults to the standard GNU make commane “make”.

`devices.cpp_standalone.openmp_spatialneuron_strategy` = `None`

> DEPRECATED. Previously used to chose the strategy to parallelize the solution of the three tridiagonal systems for multicompartmental neurons. Now, its value is ignored.

`devices.cpp_standalone.openmp_threads` = `0`

> The number of threads to use if OpenMP is turned on. By default, this value is set to 0 and the C++ code is generated without any reference to OpenMP. If greater than 0, then the corresponding number of threads are used to launch the simulation.

`devices.cpp_standalone.run_cmd_unix` = `'./main'`

> The command used to run the compiled standalone project. Defaults to executing the compiled binary with “./main”. Must be a single binary as string or a list of command arguments (e.g. [“./binary”, “–key”, “value”]).

`devices.cpp_standalone.run_environment_variables` = `{'LD_BIND_NOW': '1'}`

> Dictionary of environment variables and their values that will be set during the execution of the standalone code.

### legacy

Preferences to enable legacy behaviour

`legacy.refractory_timing` = `False`

> Whether to use the semantics for checking the refractoriness condition that were in place up until (including) version 2.1.2. In that implementation, refractory periods that were multiples of dt could lead to a varying number of refractory timesteps due to the nature of floating point comparisons). This preference is only provided for exact reproducibility of previously obtained results, new simulations should use the improved mechanism which uses a more robust mechanism to convert refractoriness into timesteps. Defaults to `False`.

### logging

Logging system preferences

`logging.console_log_level` = `'INFO'`

> What log level to use for the log written to the console.
> 
> Has to be one of CRITICAL, ERROR, WARNING, INFO, DEBUG or DIAGNOSTIC.

`logging.delete_log_on_exit` = `True`

> Whether to delete the log and script file on exit.
> 
> If set to `True` (the default), log files (and the copy of the main script) will be deleted after the brian process has exited, unless an uncaught exception occurred. If set to `False`, all log files will be kept.

`logging.display_brian_error_message` = `True`

> Whether to display a text for uncaught errors, mentioning the location of the log file, the mailing list and the github issues.
> 
> Defaults to `True`.

`logging.file_log` = `True`

> Whether to log to a file or not.
> 
> If set to `True` (the default), logging information will be written to a file. The log level can be set via the [logging.file_log_level](../reference/brian2.utils.html#brian-pref-logging-file-log-level) preference.

`logging.file_log_level` = `'DEBUG'`

> What log level to use for the log written to the log file.
> 
> In case file logging is activated (see [logging.file_log](../reference/brian2.utils.html#brian-pref-logging-file-log)), which log level should be used for logging. Has to be one of CRITICAL, ERROR, WARNING, INFO, DEBUG or DIAGNOSTIC.

`logging.file_log_max_size` = `10000000`

> The maximum size for the debug log before it will be rotated.
> 
> If set to any value `> 0`, the debug log will be rotated once this size is reached. Rotating the log means that the old debug log will be moved into a file in the same directory but with suffix `".1"` and the a new log file will be created with the same pathname as the original file. Only one backup is kept; if a file with suffix `".1"` already exists when rotating, it will be overwritten. If set to `0`, no log rotation will be applied. The default setting rotates the log file after 10MB.

`logging.save_script` = `True`

> Whether to save a copy of the script that is run.
> 
> If set to `True` (the default), a copy of the currently run script is saved to a temporary location. It is deleted after a successful run (unless [logging.delete_log_on_exit](../reference/brian2.utils.html#brian-pref-logging-delete-log-on-exit) is `False`) but is kept after an uncaught exception occured. This can be helpful for debugging, in particular when several simulations are running in parallel.

`logging.std_redirection` = `True`

> Whether or not to redirect stdout/stderr to null at certain places.
> 
> This silences a lot of annoying compiler output, but will also hide error messages making it harder to debug problems. You can always temporarily switch it off when debugging. If [logging.std_redirection_to_file](../reference/brian2.utils.html#brian-pref-logging-std-redirection-to-file) is set to `True` as well, then the output is saved to a file and if an error occurs the name of this file will be printed.

`logging.std_redirection_to_file` = `True`

> Whether to redirect stdout/stderr to a file.
> 
> If both `logging.std_redirection` and this preference are set to `True`, all standard output/error (most importantly output from the compiler) will be stored in files and if an error occurs the name of this file will be printed. If [logging.std_redirection](../reference/brian2.utils.html#brian-pref-logging-std-redirection) is `True` and this preference is `False`, then all standard output/error will be completely suppressed, i.e. neither be displayed nor stored in a file.
> 
> The value of this preference is ignore if [logging.std_redirection](../reference/brian2.utils.html#brian-pref-logging-std-redirection) is set to `False`.

---

# Random numbers2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/advanced/random.html

# Random numbers

Brian provides two basic functions to generate random numbers that can be used in model code and equations: `rand()`, to generate uniformly generated random numbers between 0 and 1, and `randn()`, to generate random numbers from a standard normal distribution (i.e. normally distributed numbers with a mean of 0 and a standard deviation of 1). All other stochastic elements of a simulation (probabilistic connections, Poisson-distributed input generated by [`PoissonGroup`](../reference/brian2.input.poissongroup.PoissonGroup.html#brian2.input.poissongroup.PoissonGroup "brian2.input.poissongroup.PoissonGroup") or [`PoissonInput`](../reference/brian2.input.poissoninput.PoissonInput.html#brian2.input.poissoninput.PoissonInput "brian2.input.poissoninput.PoissonInput"), differential equations using the noise term `xi`, …) will internally make use of these two basic functions.

For [Runtime code generation](../user/computation.html#runtime), random numbers are generated by [`numpy.random.rand`](https://numpy.org/doc/stable/reference/random/generated/numpy.random.rand.html#numpy.random.rand "\(in NumPy v2.0\)") and [`numpy.random.randn`](https://numpy.org/doc/stable/reference/random/generated/numpy.random.randn.html#numpy.random.randn "\(in NumPy v2.0\)") respectively, which uses a [Mersenne-Twister](https://en.wikipedia.org/wiki/Mersenne_Twister) pseudorandom number generator. When the `numpy` code generation target is used, these functions are called directly, but for `cython`, Brian uses a internal buffers for uniformly and normally distributed random numbers and calls the numpy functions whenever all numbers from this buffer have been used. This avoids the overhead of switching between C code and Python code for each random number. For [Standalone code generation](../user/computation.html#cpp-standalone), the random number generation is based on “randomkit”, the same Mersenne-Twister implementation that is used by numpy. The source code of this implementation will be included in every generated standalone project.

## Seeding and reproducibility

### Runtime mode

As explained above, [Runtime code generation](../user/computation.html#runtime) makes use of numpy’s random number generator. In principle, using [`numpy.random.seed`](https://numpy.org/doc/stable/reference/random/generated/numpy.random.seed.html#numpy.random.seed "\(in NumPy v2.0\)") therefore permits reproducing a stream of random numbers. However, for `cython`, Brian’s buffer complicates the matter a bit: if a simulation sets numpy’s seed, uses 10000 random numbers, and then resets the seed, the following 10000 random numbers (assuming the current size of the buffer) will come out of the pre-generated buffer before numpy’s random number generation functions are called again and take into account the seed set by the user. Instead, users should use the [`seed()`](../reference/brian2.devices.device.seed.html#brian2.devices.device.seed "brian2.devices.device.seed") function provided by Brian 2 itself, this will take care of setting numpy’s random seed _and_ empty Brian’s internal buffers. This function also has the advantage that it will continue to work when the simulation is switched to standalone code generation (see below). Note that random numbers are not guaranteed to be reproducible across different code generation targets or different versions of Brian, especially if several sources of randomness are used in the same `CodeObject` (e.g. two noise variables in the equations of a [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup")). This is because Brian does not guarantee the order of certain operations (e.g. should it first generate all random numbers for the first noise variable for all neurons, followed by the random numbers for the second noise variable for all neurons or rather first the random numbers for all noice variables of the first neuron, then for the second neuron, etc.) Since all random numbers are coming from the same stream of random numbers, the order of getting the numbers out of this stream matter.

### Standalone mode

For [Standalone code generation](../user/computation.html#cpp-standalone), Brian’s [`seed()`](../reference/brian2.devices.device.seed.html#brian2.devices.device.seed "brian2.devices.device.seed") function will insert code to set the random number generator seed into the generated code. The code will be generated at the position where the [`seed()`](../reference/brian2.devices.device.seed.html#brian2.devices.device.seed "brian2.devices.device.seed") call was made, allowing detailed control over the seeding. For example the following code would generate identical initial conditions every time it is run, but the noise generated by the `xi` variable would differ:
    
    
    G = NeuronGroup(10, 'dv/dt = -v/(10*ms) + 0.1*xi/sqrt(ms) : 1')
    seed(4321)
    G.v = 'rand()'
    seed()
    run(100*ms)
    

Note

In standalone mode, [`seed()`](../reference/brian2.devices.device.seed.html#brian2.devices.device.seed "brian2.devices.device.seed") will not set numpy’s random number generator. If you use random numbers in the Python script itself (e.g. to generate a list of synaptic connections that will be passed to the standalone code as a pre-calculated array), then you have to explicitly call [`numpy.random.seed`](https://numpy.org/doc/stable/reference/random/generated/numpy.random.seed.html#numpy.random.seed "\(in NumPy v2.0\)") yourself to make these random numbers reproducible.

Note

Seeding _should_ lead to reproducible random numbers even when using OpenMP with multiple threads (for repeated simulations with the same number of threads), but this has not been rigorously tested. Use at your own risk.

---

# Recording during a simulation2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/user/recording.html

# Recording during a simulation  
  
For Brian 1 users

See the document [Monitors (Brian 1 –> 2 conversion)](../introduction/brian1_to_2/monitors.html) for details how to convert Brian 1 code.

  * Recording spikes

  * Recording variables at spike time

  * Recording variables continuously

  * Recording population rates

  * Getting all data

  * Recording values for a subset of the run

  * Freeing up memory in long recordings

  * Recording random subsets of neurons

  * Recording population averages

Recording variables during a simulation is done with “monitor” objects. Specifically, spikes are recorded with [`SpikeMonitor`](../reference/brian2.monitors.spikemonitor.SpikeMonitor.html#brian2.monitors.spikemonitor.SpikeMonitor "brian2.monitors.spikemonitor.SpikeMonitor"), the time evolution of variables with [`StateMonitor`](../reference/brian2.monitors.statemonitor.StateMonitor.html#brian2.monitors.statemonitor.StateMonitor "brian2.monitors.statemonitor.StateMonitor") and the firing rate of a population of neurons with [`PopulationRateMonitor`](../reference/brian2.monitors.ratemonitor.PopulationRateMonitor.html#brian2.monitors.ratemonitor.PopulationRateMonitor "brian2.monitors.ratemonitor.PopulationRateMonitor").

## Recording spikes

To record spikes from a group `G` simply create a [`SpikeMonitor`](../reference/brian2.monitors.spikemonitor.SpikeMonitor.html#brian2.monitors.spikemonitor.SpikeMonitor "brian2.monitors.spikemonitor.SpikeMonitor") via `SpikeMonitor(G)`. After the simulation, you can access the attributes `i`, `t`, `num_spikes` and `count` of the monitor. The `i` and `t` attributes give the array of neuron indices and times of the spikes. For example, if `M.i==[0, 2, 1]` and `M.t==[1*ms, 2*ms, 3*ms]` it means that neuron 0 fired a spike at 1 ms, neuron 2 fired a spike at 2 ms, and neuron 1 fired a spike at 3 ms. Alternatively, you can also call the [`spike_trains`](../reference/brian2.monitors.spikemonitor.SpikeMonitor.html#brian2.monitors.spikemonitor.SpikeMonitor.spike_trains "brian2.monitors.spikemonitor.SpikeMonitor.spike_trains") method to get a dictionary mapping neuron indices to arrays of spike times, i.e. in the above example, `spike_trains = M.spike_trains(); spike_trains[1]` would return `array([ 3.]) * msecond`. The `num_spikes` attribute gives the total number of spikes recorded, and `count` is an array of the length of the recorded group giving the total number of spikes recorded from each neuron.

Example:
    
    
    G = NeuronGroup(N, model='...')
    M = SpikeMonitor(G)
    run(runtime)
    plot(M.t/ms, M.i, '.')
    

If you are only interested in summary statistics but not the individual spikes, you can set the `record` argument to `False`. You will then not have access to `i` and `t` but you can still get the `count` and the total number of spikes (`num_spikes`).

## Recording variables at spike time

By default, a [`SpikeMonitor`](../reference/brian2.monitors.spikemonitor.SpikeMonitor.html#brian2.monitors.spikemonitor.SpikeMonitor "brian2.monitors.spikemonitor.SpikeMonitor") only records the time of the spike and the index of the neuron that spiked. Sometimes it can be useful to addtionaly record other variables, e.g. the membrane potential for models where the threshold is not at a fixed value. This can be done by providing an extra `variables` argument, the recorded variable can then be accessed as an attribute of the [`SpikeMonitor`](../reference/brian2.monitors.spikemonitor.SpikeMonitor.html#brian2.monitors.spikemonitor.SpikeMonitor "brian2.monitors.spikemonitor.SpikeMonitor"), e.g.:
    
    
    G = NeuronGroup(10, 'v : 1', threshold='rand()<100*Hz*dt')
    G.run_regularly('v = rand()')
    M = SpikeMonitor(G, variables=['v'])
    run(100*ms)
    plot(M.t/ms, M.v, '.')
    

To conveniently access the values of a recorded variable for a single neuron, the [`SpikeMonitor.values`](../reference/brian2.monitors.spikemonitor.SpikeMonitor.html#brian2.monitors.spikemonitor.SpikeMonitor.values "brian2.monitors.spikemonitor.SpikeMonitor.values") method can be used that returns a dictionary with the values for each neuron.:
    
    
    G = NeuronGroup(N, '''dv/dt = (1-v)/(10*ms) : 1
                          v_th : 1''',
                    threshold='v > v_th',
                    # randomly change the threshold after a spike:
                    reset='''v=0
                             v_th = clip(v_th + rand()*0.2 - 0.1, 0.1, 0.9)''')
    G.v_th = 0.5
    spike_mon = SpikeMonitor(G, variables='v')
    run(1*second)
    v_values = spike_mon.values('v')
    print('Threshold crossing values for neuron 0: {}'.format(v_values[0]))
    hist(spike_mon.v, np.arange(0, 1, .1))
    show()
    

Note

Spikes are not the only events that can trigger recordings, see [Custom events](../advanced/custom_events.html).

## Recording variables continuously

To record how a variable evolves over time, use a [`StateMonitor`](../reference/brian2.monitors.statemonitor.StateMonitor.html#brian2.monitors.statemonitor.StateMonitor "brian2.monitors.statemonitor.StateMonitor"), e.g. to record the variable `v` at every time step and plot it for neuron 0:
    
    
    G = NeuronGroup(...)
    M = StateMonitor(G, 'v', record=True)
    run(...)
    plot(M.t/ms, M.v[0]/mV)
    

In general, you specify the group, variables and indices you want to record from. You specify the variables with a string or list of strings, and the indices either as an array of indices or `True` to record all indices (but beware because this may take a lot of memory).

After the simulation, you can access these variables as attributes of the monitor. They are 2D arrays with shape `(num_indices, num_times)`. The special attribute `t` is an array of length `num_times` with the corresponding times at which the values were recorded.

Note that you can also use [`StateMonitor`](../reference/brian2.monitors.statemonitor.StateMonitor.html#brian2.monitors.statemonitor.StateMonitor "brian2.monitors.statemonitor.StateMonitor") to record from [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses") where the indices are the synapse indices rather than neuron indices.

In this example, we record two variables v and u, and record from indices 0, 10 and 100. Afterwards, we plot the recorded values of v and u from neuron 0:
    
    
    G = NeuronGroup(...)
    M = StateMonitor(G, ('v', 'u'), record=[0, 10, 100])
    run(...)
    plot(M.t/ms, M.v[0]/mV, label='v')
    plot(M.t/ms, M.u[0]/mV, label='u')
    

There are two subtly different ways to get the values for specific neurons: you can either index the 2D array stored in the attribute with the variable name (as in the example above) or you can index the monitor itself. The former will use an index relative to the recorded neurons (e.g. `M.v[1]` will return the values for the second _recorded_ neuron which is the neuron with the index 10 whereas `M.v[10]` would raise an error because only three neurons have been recorded), whereas the latter will use an absolute index corresponding to the recorded group (e.g. `M[1].v` will raise an error because the neuron with the index 1 has not been recorded and `M[10].v` will return the values for the neuron with the index 10). If all neurons have been recorded (e.g. with `record=True`) then both forms give the same result.

Note that for plotting all recorded values at once, you have to transpose the variable values:
    
    
    plot(M.t/ms, M.v.T/mV)
    

Note

In contrast to Brian 1, the values are recorded at the beginning of a time step and not at the end (you can set the `when` argument when creating a [`StateMonitor`](../reference/brian2.monitors.statemonitor.StateMonitor.html#brian2.monitors.statemonitor.StateMonitor "brian2.monitors.statemonitor.StateMonitor"), details about scheduling can be found here: [Custom progress reporting](../advanced/scheduling.html)).

## Recording population rates

To record the time-varying firing rate of a population of neurons use [`PopulationRateMonitor`](../reference/brian2.monitors.ratemonitor.PopulationRateMonitor.html#brian2.monitors.ratemonitor.PopulationRateMonitor "brian2.monitors.ratemonitor.PopulationRateMonitor"). After the simulation the monitor will have two attributes `t` and `rate`, the latter giving the firing rate at each time step corresponding to the time in `t`. For example:
    
    
    G = NeuronGroup(...)
    M = PopulationRateMonitor(G)
    run(...)
    plot(M.t/ms, M.rate/Hz)
    

To get a smoother version of the rate, use [`PopulationRateMonitor.smooth_rate`](../reference/brian2.monitors.ratemonitor.PopulationRateMonitor.html#brian2.monitors.ratemonitor.PopulationRateMonitor.smooth_rate "brian2.monitors.ratemonitor.PopulationRateMonitor.smooth_rate").

The following topics are not essential for beginners.

  

## Getting all data

Note that all monitors are implement as “groups”, so you can get all the stored values in a monitor with the [`get_states`](../reference/brian2.groups.group.VariableOwner.html#brian2.groups.group.VariableOwner.get_states "brian2.groups.group.VariableOwner.get_states") method, which can be useful to dump all recorded data to disk, for example:
    
    
    import pickle
    group = NeuronGroup(...)
    state_mon = StateMonitor(group, 'v', record=...)
    run(...)
    data = state_mon.get_states(['t', 'v'])
    with open('state_mon.pickle', 'w') as f:
        pickle.dump(data, f)
    

## Recording values for a subset of the run

Monitors can be created and deleted between runs, e.g. to ignore the first second of your simulation in your recordings you can do:
    
    
    # Set up network without monitor
    run(1*second)
    state_mon = StateMonitor(....)
    run(...)  # Continue run and record with the StateMonitor
    

Alternatively, you can set the monitor’s [`active`](../reference/brian2.core.base.BrianObject.html#brian2.core.base.BrianObject.active "brian2.core.base.BrianObject.active") attribute as explained in the [Scheduling](running.html#scheduling) section.

## Freeing up memory in long recordings

Creating and deleting monitors can also be useful to free memory during a long recording. The following will do a simulation run, dump the monitor data to disk, delete the monitor and finally continue the run with a new monitor:
    
    
    import pickle
    # Set up network
    state_mon = StateMonitor(...)
    run(...)  # a long run
    data = state_mon.get_states(...)
    with open('first_part.data', 'w') as f:
        pickle.dump(data, f)
    del state_mon
    del data
    state_mon = StateMonitor(...)
    run(...)  # another long run
    

Note that this technique cannot be applied in [standalone mode](computation.html#cpp-standalone).

## Recording random subsets of neurons

In large networks, you might only be interested in the activity of a random subset of neurons. While you can specify a `record` argument for a [`StateMonitor`](../reference/brian2.monitors.statemonitor.StateMonitor.html#brian2.monitors.statemonitor.StateMonitor "brian2.monitors.statemonitor.StateMonitor") that allows you to select a subset of neurons, this is not possible for [`SpikeMonitor`](../reference/brian2.monitors.spikemonitor.SpikeMonitor.html#brian2.monitors.spikemonitor.SpikeMonitor "brian2.monitors.spikemonitor.SpikeMonitor")/[`EventMonitor`](../reference/brian2.monitors.spikemonitor.EventMonitor.html#brian2.monitors.spikemonitor.EventMonitor "brian2.monitors.spikemonitor.EventMonitor") and [`PopulationRateMonitor`](../reference/brian2.monitors.ratemonitor.PopulationRateMonitor.html#brian2.monitors.ratemonitor.PopulationRateMonitor "brian2.monitors.ratemonitor.PopulationRateMonitor"). However, Brian allows you to record with these monitors from a subset of neurons by using a [subgroup](models.html#subgroups):
    
    
    group = NeuronGroup(1000, ...)
    spike_mon = SpikeMonitor(group[:100])  # only record first 100 neurons
    

It might seem like a restriction that such a subgroup has to be contiguous, but the order of neurons in a group does not have any meaning as such; in a randomly ordered group of neurons, any contiguous group of neurons can be considered a random subset. If some aspects of your model _do_ depend on the position of the neuron in a group (e.g. a ring model, where neurons are connected based on their distance in the ring, or a model where initial values or parameters span a range of values in a regular fashion), then this requires an extra step: instead of using the order of neurons in the group directly, or depending on the neuron index `i`, create a new, shuffled, index variable as part of the model definition and then depend on this index instead:
    
    
    group = NeuronGroup(10000, '''....
                                  index : integer (constant)''')
    indices = group.i[:]
    np.random.shuffle(indices)
    group.index = indices
    # Then use 'index' in string expressions or use it as an index array
    # for initial values/parameters defined as numpy arrays
    

If this solution is not feasible for some reason, there is another approach that works for a [`SpikeMonitor`](../reference/brian2.monitors.spikemonitor.SpikeMonitor.html#brian2.monitors.spikemonitor.SpikeMonitor "brian2.monitors.spikemonitor.SpikeMonitor")/[`EventMonitor`](../reference/brian2.monitors.spikemonitor.EventMonitor.html#brian2.monitors.spikemonitor.EventMonitor "brian2.monitors.spikemonitor.EventMonitor"). You can add an additional flag to each neuron, stating whether it should be recorded or not. Then, you define a new [custom event](../advanced/custom_events.html) that is identical to the event you are interested in, but additionally requires the flag to be set. E.g. to only record the spikes of neurons with the `to_record` attribute set:
    
    
    group = NeuronGroup(..., '''...
                                to_record : boolean (constant)''',
                        threshold='...', reset='...',
                        events={'recorded_spike': '... and to_record'})
    group.to_record = ...
    mon_events = EventMonitor(group, 'recorded_spike')
    

Note that this solution will evaluate the threshold condition for each neuron twice, and is therefore slightly less efficient. There’s one additional caveat: you’ll have to manually include `and not_refractory` in your `events` definition if your neuron uses refractoriness. This is done automatically for the `threshold` condition, but not for any user-defined events.

## Recording population averages

Continuous recordings from large groups over long simulation times can fill up the working memory quickly: recording a single variable from 1000 neurons for 100 seconds at the default time resolution results in an array of about 8 Gigabytes. While this issue can be ameliorated using the above approaches, the downstream data analysis is often based on population averages. These can be recorded efficiently using a dummy group and the [`Synapses`](../reference/brian2.synapses.synapses.Synapses.html#brian2.synapses.synapses.Synapses "brian2.synapses.synapses.Synapses") class’ [summed variable syntax](synapses.html#summed-variables):
    
    
    group = NeuronGroup(..., 'dv/dt = ... : volt', ...)
    
    # Dummy group to store the average membrane potential at every time step
    vm_container = NeuronGroup(1, 'average_vm : volt')
    
    # Synapses averaging the membrane potential of all neurons in group
    vm_averager = Synapses(group, vm_container, 'average_vm_post = v_pre/N_pre : volt (summed)')
    vm_averager.connect()
    
    # Monitor recording the average membrane potential
    vm_monitor = StateMonitor(vm_container, 'average_vm', record=True)
    

---

# Refractoriness2.7.1 documentation

Source: https://brian2.readthedocs.io/en/stable/user/refractoriness.html

# Refractoriness

  * Defining the refractory period

  * Defining model behaviour during refractoriness

  * Arbitrary refractoriness

Brian allows you to model the absolute refractory period of a neuron in a flexible way. The definition of refractoriness consists of two components: the amount of time after a spike that a neuron is considered to be refractory, and what changes in the neuron during the refractoriness.

## Defining the refractory period

The refractory period is specified by the `refractory` keyword in the [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") initializer. In the simplest case, this is simply a fixed time, valid for all neurons:
    
    
    G = NeuronGroup(N, model='...', threshold='...', reset='...',
                    refractory=2*ms)
    

Alternatively, it can be a string expression that evaluates to a time. This expression will be evaluated after every spike and allows for a varying refractory period. For example, the following will set the refractory period to a random duration between 1ms and 3ms after every spike:
    
    
    G = NeuronGroup(N, model='...', threshold='...', reset='...',
                    refractory='(1 + 2*rand())*ms')
    

In general, modelling a refractory period that varies across neurons involves declaring a state variable that stores the refractory period per neuron as a model parameter. The refractory expression can then refer to this parameter:
    
    
    G = NeuronGroup(N, model='''...
                                ref : second''', threshold='...',
                    reset='...', refractory='ref')
    # Set the refractory period for each cell
    G.ref = ...
    

This state variable can also be a dynamic variable itself. For example, it can serve as an adaptation mechanism by increasing it after every spike and letting it relax back to a steady-state value between spikes:
    
    
    refractory_0 = 2*ms
    tau_refractory = 50*ms
    G = NeuronGroup(N, model='''...
                                dref/dt = (refractory_0 - ref) / tau_refractory : second''',
                    threshold='...', refractory='ref',
                    reset='''...
                             ref += 1*ms''')
    G.ref = refractory_0
    

In some cases, the condition for leaving the refractory period is not easily expressed as a certain time span. For example, in a Hodgkin-Huxley type model the threshold is only used for _counting_ spikes and the refractoriness is used to prevent the count of multiple spikes for a single threshold crossing (the threshold condition would evaluate to `True` for several time points). When a neuron should leave the refractory period is not easily expressed as a time span but more naturally as a condition that the neuron should remain refractory for as long as it stays above the threshold. This can be achieved by using a string expression for the `refractory` keyword that evaluates to a boolean condition:
    
    
    G = NeuronGroup(N, model='...', threshold='v > -20*mV',
                    refractory='v >= -20*mV')
    

The `refractory` keyword should be read as “stay refractory as long as the condition remains true”. In fact, specifying a time span for the refractoriness will be automatically transformed into a logical expression using the current time `t` and the time of the last spike `lastspike`. Specifying `refractory=2*ms` is basically equivalent to specifying `refractory='(t - lastspike) <= 2*ms'`. However, this expression can give inconsistent results for the common case that the refractory period is a multiple of the simulation timestep. Due to floating point impreciseness, the actual value of `t - lastspike` can be slightly above or below a multiple of the simulation time step; comparing it directly to the refractory period can therefore lead to an end of the refractory one time step sooner or later. To avoid this issue, the actual code used for the above example is equivalent to `refractory='timestep(t - lastspike, dt) <= timestep(2*ms, dt)'`. The [`timestep`](../reference/brian2.core.functions.timestep.html#brian2.core.functions.timestep "brian2.core.functions.timestep") function is provided by Brian and takes care of converting a time into a time step in a safe way.

Added in version 2.1.3: The `timestep` function is now used to avoid floating point issues in the refractoriness calculation. To restore the previous behaviour, set the [legacy.refractory_timing](../advanced/preferences.html#brian-pref-legacy-refractory-timing) preference to `True`.

## Defining model behaviour during refractoriness

The refractoriness definition as described above only has a single effect by itself: threshold crossings during the refractory period are ignored. In the following model, the variable `v` continues to update during the refractory period but it does not elicit a spike if it crosses the threshold:
    
    
    G = NeuronGroup(N, 'dv/dt = -v / tau : 1',
                    threshold='v > 1', reset='v=0',
                    refractory=2*ms)
    

There is also a second implementation of refractoriness that is supported by Brian, one or several state variables can be clamped during the refractory period. To model this kind of behaviour, variables that should stop being updated during refractoriness can be marked with the `(unless refractory)` flag:
    
    
    G = NeuronGroup(N, '''dv/dt = -(v + w)/ tau_v : 1 (unless refractory)
                          dw/dt = -w / tau_w : 1''',
                    threshold='v > 1', reset='v=0; w+=0.1', refractory=2*ms)
    

In the above model, the `v` variable is clamped at 0 for 2ms after a spike but the adaptation variable `w` continues to update during this time. In addition, a variable of a neuron that is in its refractory period is _read-only_ : incoming synapses or other code will have no effect on the value of `v` until it leaves its refractory period.

The following topics are not essential for beginners.

  

## Arbitrary refractoriness

In fact, arbitrary behaviours can be defined using Brian’s refractoriness mechanism.

A [`NeuronGroup`](../reference/brian2.groups.neurongroup.NeuronGroup.html#brian2.groups.neurongroup.NeuronGroup "brian2.groups.neurongroup.NeuronGroup") with refractoriness automatically defines two variables:

`not_refractory`
    

A boolean variable stating whether a neuron is allowed to spike.

`lastspike`
    

The time of the last spike of the neuron.

The variable `not_refractory` is updated at every time step by checking the refractoriness condition – for a refractoriness defined by a time period, this means comparing `lastspike` to the current time `t`. The `not_refractory` variable is then used to implement the refractoriness behaviour. Specifically, the `threshold` condition is replaced by `threshold and not_refractory` and differential equations that are marked as `(unless refractory)` are multiplied by `int(not_refractory)` (so that they have the value 0 when the neuron is refractory).

This `not_refractory` variable is also available to the user to define more sophisticated refractoriness behaviour. For example, the following code updates the `w` variable with a different time constant during refractoriness:
    
    
    G = NeuronGroup(N, '''dv/dt = -(v + w)/ tau_v : 1 (unless refractory)
                          dw/dt = (-w / tau_active)*int(not_refractory) + (-w / tau_ref)*(1 - int(not_refractory)) : 1''',
                    threshold='v > 1', reset='v=0; w+=0.1', refractory=2*ms)
