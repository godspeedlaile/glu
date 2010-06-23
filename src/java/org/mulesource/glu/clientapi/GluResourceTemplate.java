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

import java.util.HashMap;

/**
 * Represents a template that can be used by a client to create a new resource.
 *
 * This representation can be used by clients to find out about
 * component capabilities and also as a starting point to create
 * new resources, by utilizing the getResourceTemplate() method.
 */
public class GluResourceTemplate
{
    protected final static String     PARAMS_KEY             = "params";
    protected final static String     RCP_KEY                = "resource_creation_params";
    protected final static String     RCP_DESC_KEY           = "desc";
    protected final static String     RCP_SUGGESTED_NAME_KEY = "suggested_name";

    protected GluComponent            component;
    protected HashMap<String, Object> paramValues;
    protected HashMap<String, Object> resourceCreationParamValues;

    /**
     * Create a new resource template in memory.
     *
     * @param component  The GluComponent which created this template.
     */
    public GluResourceTemplate(GluComponent component)
    {
        this.component              = component;
        paramValues                 = new HashMap<String, Object>();
        resourceCreationParamValues = new HashMap<String, Object>();
    }
    
    /**
     * Returns all parameters defined for this template's component.
     * 
     * @return  Map of parameters.
     */
    public HashMap<String, GluParameter> getAllParameters()
    {
        return component.getAllParameters();
    }
    
    /**
     * Return one parameter of this template's component.
     * 
     * @param  name  Name of the parameter.
     * @return       Representation of this parameter.
     */
    public GluParameter getParameter(String name)
    {
        return component.getParameter(name);
    }
    
    /**
     * Return parameter definition for this template's resource description parameter.
     * 
     * @return  Representation of this parameter.
     */
    public GluParameter getResourceDescription()
    {
        return component.getResourceDescription();
    }

    /**
     * Return parameter definition for this template's suggested name parameter.
     * 
     * @return  Representation of this parameter.
     */
    public GluParameter getResourceSuggestedName()
    {
        return component.getSuggestedName();
    }
    
    /**
     * Set a parameter value for a given parameter.
     *
     * Performs proper sanity checking on the type and value.
     *
     * @param name   Name of the parameter.
     * @param value  Value object for that parameter.
     * 
     * @return       Reference to ourselves so that set() calls can be chained.
     * 
     * @throws       GluClientException
     */
    public GluResourceTemplate set(String name, Object value) throws GluClientException
    {
        GluParameter pdef = getParameter(name);
        pdef.sanityCheck(value);
        paramValues.put(name, value);
        return this;
    }
    
    /**
     * Sets the 'description' resource creation time parameter.
     * 
     * @param  desc  The description for the new resource.
     * @return       Reference to ourselves so that set...() calls can be chained.
     */
    public GluResourceTemplate setDescription(String desc)
    {
        resourceCreationParamValues.put(RCP_DESC_KEY, desc);
        return this;
    }
    
    /**
     * Sets the 'suggested name' resource creation time parameter.
     * 
     * @param  name  The suggested name for the new resource.
     * @return       Reference to ourselves so that set...() calls can be chained.
     */
    public GluResourceTemplate setSuggestedName(String name)
    {
        resourceCreationParamValues.put(RCP_SUGGESTED_NAME_KEY, name);
        return this;
    }
    
    public GluResource createResource() throws GluClientException
    {
        // Check whether all required parameters have been set
        HashMap<String, GluParameter> parameters = getAllParameters();
        if (parameters != null  &&  !parameters.isEmpty()) {
            for (String pname: parameters.keySet()) {
                if (parameters.get(pname).isRequired()  &&  !paramValues.containsKey(pname)) {
                    throw new GluClientException("Required parameter '" + pname + "' is missing.");
                }
            }
        }
        
        // Assemble the resource creation dictionary, which is sent
        // to the component URI in order to create a resource on the
        // server.
        HashMap<String, Object> d = new HashMap<String, Object>();
        d.put(PARAMS_KEY, paramValues);
        d.put(RCP_KEY,    resourceCreationParamValues);
        HashMap<String, Object> res = component.createResource(d);
        
        // The server returned a dictionary with some information about
        // the outcome of the operation.
        String status = (String) res.get("status");
        if (status == null  ||  !status.equals("created")) {
            throw new GluClientException("Resource could not be created.");
        }
        
        // Quickest way for us to get the resource is to just
        // get it directly from the server, using the name we
        // were given.
        String name = (String)res.get("name");
        return component.getServer().getResource(name);
    }

}


