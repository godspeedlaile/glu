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

public class Result
{
    private int    code;
    private Object obj;
        
    public Result(int code, Object obj)
    {
        this.code = code;
        this.obj  = obj;
    }
    
    public int getCode()
    {
        return code;
    }
    
    public Object getObject()
    {
        return obj;
    }
}


