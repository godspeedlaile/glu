/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */

package org.mulesource.glu.component;

import java.math.BigDecimal;
import java.util.HashMap;
import java.util.Vector;

import org.mulesource.glu.component.api.*;
import org.mulesource.glu.exception.GluException;


@ComponentInfo(name        = "TestComponent",
               description = "This is a Java test component",
               doc         = "Here is a doc string")
public class TestComponent extends BaseComponent
{    
    @Parameter(name="api_key", desc="This is the API key")
    //@Default("foo foo foo")
    public String api_key;
    
    @Service(description = "This is the foobar service")
    public Result foobar(HttpMethod method, String input,
                         
                         @Parameter(name="query", desc="This is the query string", positional=true)
                         @Default("foo")
                         String     query,
                         
                         @Parameter(name="num", desc="The number of results", positional=true)
                         @Default("10")
                         BigDecimal num)
    {
        System.out.println("----------------------------------------------------------");
        System.out.println("### input:   " + input.getClass() + " === " + input);
        System.out.println("### method:  " + method.getClass() + " === " + method);
             
        System.out.println("Query parameter: " + query);
        System.out.println("Num parameter:   " + num);
        
        HashMap res = new HashMap();
        res.put("foo", "This is a test");
        HashMap sub = new HashMap();
        res.put("bar", sub);
        sub.put("some value", 1);
        sub.put("another value", "Some text");
        Vector v = new Vector();
        v.add("Blah");
        v.add(12345);
        sub.put("some vector", v);
        
        v = new Vector();
        v.add("Some text");
        v.add(123);
        v.add(res);
        
        return Result.ok(v);
    }
 
    @Service(description = "This accesses a Python Google search resource and returns the result")
    public Result blahblah(HttpMethod method, String input)
    {
        HttpResult res;
        HashMap params = new HashMap();
        params.put("query", "foo");
        res = accessResource("/resource/MyGoogleSearch/search", null, params);
        return new Result(res.status, res.data);
    }
}


