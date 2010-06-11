/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */

/*
 * A sample template for Glu components, written in Python.
 */

package org.mulesource.glu.component;

import java.math.BigDecimal;                 // Default type for numeric values

import org.mulesource.glu.component.api.*;   // Imports all aspects of the API

//
// If you want to handle or throw Glu specific exceptions, you might also want
// to import this:
//
// import org.mulesource.glu.exception.*;
//

// -----------------------------------------------
// Tell Glu some information about this component.
// -----------------------------------------------
@ComponentInfo(name        = "SampleComponent",
               description = "One line description of the component",
               doc         = "Longer description text, possibly multi-line, goes here")
public class SampleComponent extends BaseComponent
{    
    // ---------------------------------
    // Resource creation time parameters
    // ---------------------------------
    // Currently, only the following types are supported for parameters:
    // String, Boolean, Number

    @Parameter(name="someParameter", desc="Short description of this parameter")
    public String someParameter;    // without default: parameter is mandatory
    
    @Parameter(name="anotherParameter", desc="Short description of this parameter")
    @Default("123.4")               // default value (as string representation) is specified: parameter is optional
    public BigDecimal anotherParameter;
    
    // ---------------
    // Service methods
    // ---------------
    @Service(description = "This is the foobar service")
    public Result foobar(HttpMethod method, String input,     // These two parameters are always present
                         
                         // Here now the parameters that are exposed on the URI command line

                         // The following defines a non-positional, mandatory parameter
                         @Parameter(name="text", desc="This is a text parameter")
                         String     text,
                         
                         // This defines an optional, positional parameter. Note that positional
                         // parameters may either be set with query-type arguments on the URI
                         // command line, or as path elements in the URI.
                         @Parameter(name="num", desc="A numeric parameter", positional=true)
                         @Default("10")
                         BigDecimal num)
    {
        // -------------------------------------------------
        // Any kind of processing may take place here.
        // No restriction on the available language features
        // and accessible libraries.
        
        // -----------------------------------------------
        // BaseComponent provides a few facilities to make
        // life easier for the component author.
        //
        // Specifically:
        //
        // HTTP access:
        //     httpGet()
        //     httpPost()
        //     setCredentials()
        //
        // Storage:
        //     getFileStorage() (providing: loadFile(), storeFile(), deleteFile(), listFiles())
        //
        // Accessing other resources:
        //     accessResource()

        // -------------------------------------------------------------------------
        // Preparing return data:
        //     Result object, with convenient factory methods.
        //
        // Return data can be objects of the following types: String, Boolean,
        // Number, HashMap or ArrayList. HashMaps or ArrayLists may contain elements
        // of any of these types, including further HashMaps or ArrayLists. Thus,
        // it is possible to assemble lists or complex, hiearchical data structures
        // as return values.

        String data = "Some return value";

        return Result.ok(data);
    }
}


