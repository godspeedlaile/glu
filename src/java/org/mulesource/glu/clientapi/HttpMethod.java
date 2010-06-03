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
 * A type for the known HTTP methods.
 */
public enum HttpMethod
{
    GET,
    PUT,
    POST,
    DELETE,
    OPTIONS,
    HEAD,
    UNKNOWN;
        
    /**
     * Convert an HttpMethod to a string representation of the method.
     * 
     * @param   method    The HttpMethod instance for which we want the
     *                    string representation.
     * @return            A string representation of the HttpMethod.
     */
    public static String toString(HttpMethod method)
    {
        if (method == GET) {
            return "GET";
        }
        else if (method == PUT) {
            return "PUT";
        }
        else if (method == POST) {
            return "POST";
        }
        else if (method == DELETE) {
            return "DELETE";
        }
        else if (method == OPTIONS) {
            return "OPTIONS";
        }
        else if (method == HEAD) {
            return "HEAD";
        }
        else {
            return "UNKNOWN";
        }
    }
    
    /**
     * Create a new HttpMethod object from a string representation.
     * 
     * @param   method   String representation of the method. Must be
     *                   uppercase.
     * @return           A new HttpMethod object for this method.
     */
    public static HttpMethod fromString(String method)
    {
        if (method.equals("GET")) {
            return GET;
        }
        else if (method.equals("POST")) {
            return POST;
        }
        else if (method.equals("PUT")) {
            return PUT;
        }
        else if (method.equals("DELETE")) {
            return DELETE;
        }
        else if (method.equals("OPTIONS")) {
            return OPTIONS;
        }
        else if (method.equals("HEAD")) {
            return HEAD;
        }
        else {
            return UNKNOWN;
        }
    }
}


