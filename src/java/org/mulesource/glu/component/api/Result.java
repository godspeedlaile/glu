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

import org.mulesource.glu.exception.*;

import java.util.HashMap;

/*
 * Inspired by the Result class defined for JAX-RS
 */
public class Result
{
    private int                     code;
    private Object                  data;
    private HashMap<String, String> headers;

    
    public Result(int code, Object data)
    {
        this.code    = code;
        this.data    = data;
        this.headers = null;
    }
    
    public void addHeader(String name, String value)
    {
        if (headers == null) {
            headers = new HashMap<String, String>();
        }
        headers.put(name, value);
    }
    
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
        return created(uri, null);
    }
    
    public static Result created(String uri, Object obj)
    {
        Result res = new Result(HTTP.CREATED, obj);
        res.addHeader("Location", uri);
        return res;
    }
    
    public static Result notFound(String message)
    {
        return new Result(HTTP.NOT_FOUND, message);
    }
    
    public static Result badRequest(String message)
    {
        return new Result(HTTP.BAD_REQUEST, message);
    }
    
    public static Result noContent()
    {
        return new Result(HTTP.NO_CONTENT, null);
    }
    
    public static Result temporaryRedirect(String uri)
    {
        Result res = new Result(HTTP.TEMPORARY_REDIRECT, null);
        res.addHeader("Location", uri);
        return res;
    }
    
    public static Result internalServerError(String message)
    {
        return new Result(HTTP.INTERNAL_SERVER_ERROR, message);
    }
    
    public int getStatus()
    {
        return code;
    }
    
    public void setStatus(int code)
    {
        this.code = code;
    }
    
    public Object getEntity()
    {
        return data;
    }
    
    public void setEntity(Object data)
    {
        this.data = data;
    }
    
    public HashMap<String, String> getHeaders()
    {
        return headers;
    }
}



