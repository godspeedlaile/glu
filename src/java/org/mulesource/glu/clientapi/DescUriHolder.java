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
 * Only used here to hold description and uris of
 * components and resources.
 * 
 * When we query /code or /resource on the server, we
 * get back a dictionary of dictionaries. The second-
 * level dictionaries don't hold the full information
 * about a component or resource, but just the name
 * and URI. This class here represents that.  
 */
public class DescUriHolder
{
    public String desc;
    public String uri;
    
    /**
     * Construct a new description holder.
     * 
     * @param desc   Description of the element.
     * @param uri    URI of the element.
     */
    public DescUriHolder(String desc, String uri)
    {
        this.desc = desc;
        this.uri  = uri;
    }
}
