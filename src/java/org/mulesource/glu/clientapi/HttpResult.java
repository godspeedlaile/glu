/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */

package org.mulesource.glu.clientapi;

/**
 * The result of an HTTP request.
 */
public class HttpResult
{
    /**
     * The HTTP status that was returned for this request.
     */
    public int    status;
    
    /**
     * The data that was returned.
     * 
     * In some cases the data might have been de-serialized
     * already, which is why this is a generic Object type.
     * The caller needs to cast this data to the type it wants
     * to deal with.
     */
    public Object data;
    
    /**
     * Create a new HTTP result object.
     * 
     * @param status    The status returned by the server.
     * @param data      The data returned by the server.
     */
    public HttpResult(int status, Object data)
    {
        this.status = status;
        this.data   = data;
    }
}


