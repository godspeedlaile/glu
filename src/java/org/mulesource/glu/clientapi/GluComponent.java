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
 * Client-side representation of a component on a Glu server.
 * 
 * This can be used by clients to find out about a component
 * and its capabilities. It is also the starting point for
 * creating a new resource that's based on this component.
 */
public class GluComponent
{
    // The well-known URIs where we can find specific server information
    protected static final String            NAME_KEY               = "name";
    protected static final String            DESC_KEY               = "desc";
    protected static final String            DOC_KEY                = "doc";
    protected static final String            URI_KEY                = "uri";
    protected static final String            PARAMS_KEY             = "params";
    protected static final String            RCP_KEY                = "resource_creation_params";
    protected static final String            RCP_DESC_KEY           = "desc";
    protected static final String            RCP_SUGGESTED_NAME_KEY = "suggested_name";
    protected static final String            SERVICES_KEY           = "services";
    
    protected GluServer                      server;
    protected String                         name;
    protected String                         description;
    protected String                         docUri;
    protected String                         doc;
    protected String                         uri;
    protected HashMap<String, GluParameter>  parameters;
    protected GluParameter                   rcpDescriptionParam;
    protected GluParameter                   rcpSuggestedNameParam;
    protected HashMap<String, GluService>    services;
    
    
    /**
     * Create a new GluComponent object, representing a Glu component in the client.
     * 
     * @param   server  Reference to the client-side representation of the Glu server.
     * @param   cdesc   A map with all the information about the component.
     * @throws          GluClientException
     */
    public GluComponent(GluServer server, HashMap<String, ?> cdesc) throws GluClientException
    {
        this.server = server;
        
        // Store the meta data for later use
        try {
            name                     = (String)cdesc.get(NAME_KEY);
            description              = (String)cdesc.get(DESC_KEY);
            docUri                   = (String)cdesc.get(DOC_KEY);
            uri                      = (String)cdesc.get(URI_KEY);
            HashMap<String, ?> pdict = (HashMap<String, ?>)cdesc.get(PARAMS_KEY);
            HashMap<String, ?> sdict = (HashMap<String, ?>)cdesc.get(SERVICES_KEY);

            // Parse the parameter dictionary and attempt to translate
            // this into a dictionary of proper GluParameter objects.
            parameters = new HashMap<String, GluParameter>();
            for (String pname : pdict.keySet()) {
                parameters.put(pname, new GluParameter(pname, (HashMap<String, ?>)pdict.get(pname)));
            }
            
            // Set the resource creation time parameters, which
            // are always the same for every component. When we
            // create those parameter definitions we specify the
            // dictionary key as the name of the parameter, don't
            // be surprised...
            HashMap<String, HashMap<String, ?>> rcpMap = (HashMap<String, HashMap<String, ?>>) cdesc.get(RCP_KEY);
            rcpDescriptionParam   = new GluParameter(RCP_DESC_KEY,           rcpMap.get(RCP_DESC_KEY));
            rcpSuggestedNameParam = new GluParameter(RCP_SUGGESTED_NAME_KEY, rcpMap.get(RCP_SUGGESTED_NAME_KEY));

            // Parse the services dictionary and attempt to translate
            // this into a dictionary of proper GluService objects.
            services = new HashMap<String, GluService>();
            for (String sname : sdict.keySet()) {
                services.put(sname, new GluService(sname, (HashMap<String, ?>)sdict.get(sname)));
            }
        }
        catch (Exception e) {
            System.out.println("Exception: " + e);
            throw new GluClientException("Server error: Could not process component meta data: " + e.getMessage());
        }
    }
    
    /**
     * Sends the request to create a new resource on the server.
     * 
     * Clients don't use this method, but instead create a resource
     * through a {@link GluResourceTemplate} object.
     * 
     * This method sends a request to this components own URI.
     * 
     * @param  rdict The dictionary with all required parameters for the
     *               resource creation.
     *               
     * @return       An HttpResult object, containing the response from the server.
     * 
     * @throws       GluClientException
     */
    protected HashMap<String, Object> createResource(Object rdict) throws GluClientException
    {
        return server.createResource(uri, rdict);
    }
    
    /**
     * Returns the name of this component.
     * 
     * @return  Name of the component.
     */
    public String getName()
    {
        return name;
    }
    
    /**
     * Returns the description for this component.
     * 
     * @return  Description of the component.
     */
    public String getDescription()
    {
        return description;
    }
    
    /**
     * Return the doc page for this component.
     * 
     * This may generate a request to the server for the component's docs.
     * Once we receive the information, it is cached so that we can reused
     * it later on.
     * 
     * @return  Doc page for this component.
     * @throws  GluClientException
     */
    public String getDocs() throws GluClientException
    {
        if (doc == null) {
            HttpResult res = server.jsonSend(docUri, null, null, 200, null);
            doc = (String)res.data;
        }
        return doc;
    }
    
    /**
     * Returns reference to the GluServer for this component.
     * 
     * @return  {@link GluServer} reference.
     */
    public GluServer getServer()
    {
        return server;
    }

    /**
     * Return definition of the description parameter.
     * 
     * The description parameter is used when creating a resource.
     * 
     * @return  Definition of the description parameter.
     */
    public GluParameter getResourceDescription()
    {
        return rcpDescriptionParam;
    }

    /**
     * Return definition of the suggested name parameter.
     * 
     * The suggested name parameter is used when creating a resource.
     * 
     * @return  Definition of the suggested name parameter.
     */
    public GluParameter getSuggestedName()
    {
        return rcpSuggestedNameParam;
    }
    
    /**
     * Return a map of all the parameter definitions for this component.
     * 
     * @return  Map of {@link GluParameter} objects.
     */
    public HashMap<String, GluParameter> getAllParameters()
    {
        return parameters;
    }
    
    /**
     * Return a single parameter definition.
     * 
     * @return  A single {@link GluParameter} object.
     */
    public GluParameter getParameter(String name)
    {
        return parameters.get(name);
    }
    
    /**
     * Return a map of all the service definitions for this component.
     * 
     * @return  Map of {@link GluService} objects.
     */
    public HashMap<String, GluService> getAllServices()
    {
        return services;
    }
    
    /**
     * Returns a service object for the specified service.
     * 
     * @param  name  Name of the service.
     * @return       Object representing this service.
     */
    public GluService getService(String name)
    {
        return services.get(name);
    }
    
    /**
     * Return template for creation of new resource based on this component.
     * 
     * @return  A new resource creation template.
     */
    public GluResourceTemplate getResourceTemplate()
    {
        return new GluResourceTemplate(this);
    }
}


