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
 * Represents information about a resource on a Glu server.
 *
 * This representation can be used by clients to find out about
 * component capabilities and also as a starting point to create
 * new resources, by utilizing the get_resource_template() function.
 */
public class GluResource
{
    protected final static String                   NAME_KEY     = "name";
    protected final static String                   DESC_KEY     = "desc";
    protected final static String                   URI_KEY      = "uri";
    protected final static String                   SERVICES_KEY = "services";

    protected final static String[]                 REQUIRED_KEYS  = { NAME_KEY, DESC_KEY, URI_KEY, SERVICES_KEY };

    protected GluServer                             server;
    protected String                                name;
    protected String                                description;
    protected String                                uri;    
    protected HashMap<String, GluAccessibleService> services;
    
    /**
     * Create a new client-side resource representation.
     * 
     * @param server  The GluServer on which this resource resides.
     * @param rdesc   The dictionary describing the resource. This is the
     *                dictionary returned by the server when a resource
     *                URI is accessed.
     *                
     * @throws GluClientException
     */
    public GluResource(GluServer server, HashMap<String, ?> rdesc) throws GluClientException
    {
        this.server = server;
        try {
            // Sanity check on received information
            GluServer.checkKeyset(rdesc, REQUIRED_KEYS);

            description       = (String)rdesc.get(DESC_KEY);
            uri               = (String)rdesc.get(URI_KEY);
            
            // Parse the service dictionary and attempt to translate
            // this to a dictionary of proper GluAccessibleService objects.
            HashMap<String, HashMap<String, ?>> sdict =
                                            (HashMap<String, HashMap<String, ?>>)rdesc.get(SERVICES_KEY);
        
            services = new HashMap<String, GluAccessibleService>();
            for (String sname: sdict.keySet()) {
                services.put(sname, new GluAccessibleService(this, sname, sdict.get(sname)));
            }            
        }
        catch (GluClientException e) {
            throw new GluClientException("Malformed resource definition: " + e.getMessage());
        }
    }
    
    /**
     * Returns the name of the resource.
     * 
     * @return  Name of the resource.
     */
    public String getName()
    {
        return name;
    }

    /**
     * Returns the description of the resource.
     * 
     * @return  Description of the resource.
     */
    public String getDescription()
    {
        return description;
    }

    /**
     * Returns the URI of the resource.
     * 
     * @return  URI of the resource.
     */
    public String getUri()
    {
        return uri;
    }
    
    /**
     * Returns the server on which this resource resides.
     * 
     * @return  Reference to the Glu server.
     */
    public GluServer getServer()
    {
        return server;
    }
    
    /**
     * Returns a map of all the services offered by this resource.
     * 
     * @return  Map of services.
     */
    public HashMap<String, GluAccessibleService> getAllServices()
    {
        return services;
    }
    
    /**
     * Return one service of this resource.
     * 
     * @param   name  Name of the service.
     * @return        A Glu service object.
     * 
     * @throws        GluClientException
     */
    public GluAccessibleService getService(String name) throws GluClientException
    {
        GluAccessibleService service = services.get(name);
        if (service == null) {
            throw new GluClientException("Service '" + name + "' is not defined.");
        }
        return service;
    }
    
    /**
     * Delete this resource from the server.
     * 
     * This local object becomes unusable after this operation.
     * 
     * @throws GluClientException
     */
    public void delete() throws GluClientException
    {
        server.send(uri, null, HttpMethod.DELETE, 200, null);
    }
}


