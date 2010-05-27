/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */

package org.mulesource.glu.component.api;

import java.util.HashMap;

/*
 * Inspired by the Result class defined for JAX-RS
 */
public class Result
{
    private int                     code;
    private Object                  data;
    private HashMap<String, String> headers;
        
    public static Result ok()
    {
        return new Result(HTTP.OK, null);
    }
    
    public static Result ok(Object data)
    {
        return new Result(HTTP.OK, data);
    }
    
    public static Result created(String uri)
    {
        Result res = new Result(HTTP.CREATED, null);
        res.headers.put("Location", uri);
        return res;
    }
    
    public static Result noContent()
    {
        return new Result(HTTP.NO_CONTENT, null);
    }
    
    public static Result temporaryRedirect(String uri)
    {
        Result res = new Result(HTTP.TEMPORARY_REDIRECT, null);
        res.headers.put("Location", uri);
        return res;
    }
    
    public Result(int code, Object data)
    {
        this.code = code;
        this.data  = data;
    }
    
    public int getStatus()
    {
        return code;
    }
    
    public Object getEntity()
    {
        return data;
    }
    
    public HashMap<String, String> getHeaders()
    {
        return headers;
    }
}



