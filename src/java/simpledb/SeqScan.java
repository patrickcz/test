package simpledb;

import java.util.*;

/**
 * SeqScan is an implementation of a sequential scan access method that reads
 * each tuple of a table in no particular order (e.g., as they are laid out on
 * disk).
 */
public class SeqScan implements DbIterator {

    private static final long serialVersionUID = 1L;
    
    private final TransactionId transactionId;
    private int tableId;
    private String tableAlias;
    private DbFileIterator fileIter;
    
    private TupleDesc tupleDesc;
    
    private TupleDesc attachAlias(TupleDesc td, String alias){
        int numFields = td.numFields();
        String[] nameAr = new String[numFields];
        Type[] typeAr = new Type[numFields];
        for(int i=0; i<numFields; i++){
            nameAr[i] = alias + "." + td.getFieldName(i);
            typeAr[i] = td.getFieldType(i);
        }
        return new TupleDesc(typeAr, nameAr);
    
    }
    /**
     * Creates a sequential scan over the specified table as a part of the
     * specified transaction.
     *
     * @param tid
     *            The transaction this scan is running as a part of.
     * @param tableid
     *            the table to scan.
     * @param tableAlias
     *            the alias of this table (needed by the parser); the returned
     *            tupleDesc should have fields with name tableAlias.fieldName
     *            (note: this class is not responsible for handling a case where
     *            tableAlias or fieldName are null. It shouldn't crash if they
     *            are, but the resulting name can be null.fieldName,
     *            tableAlias.null, or null.null).
     */
    public SeqScan(TransactionId tid, int tableid, String tableAlias) {
        // some code goes here   
        this.transactionId = tid;
        this.tableId = tableid;
        this.tableAlias = tableAlias;
        this.fileIter = Database.getCatalog().getDatabaseFile(tableid).iterator(transactionId);
        this.tupleDesc = this.attachAlias(Database.getCatalog().getTupleDesc(tableid), tableAlias);
    }

    /**
     * @return
     *       return the table name of the table the operator scans. This should
     *       be the actual name of the table in the catalog of the database
     * */
    public String getTableName() {
        return Database.getCatalog().getTableName(this.tableId);   //???
    }

    /**
     * @return Return the alias of the table this operator scans.
     * */
    public String getAlias()
    {
        // some code goes here   
        return this.tableAlias;
    }

    /**
     * Reset the tableid, and tableAlias of this operator.
     * @param tableid
     *            the table to scan.
     * @param tableAlias
     *            the alias of this table (needed by the parser); the returned
     *            tupleDesc should have fields with name tableAlias.fieldName
     *            (note: this class is not responsible for handling a case where
     *            tableAlias or fieldName are null. It shouldn't crash if they
     *            are, but the resulting name can be null.fieldName,
     *            tableAlias.null, or null.null).
     */
    public void reset(int tableid, String tableAlias) {
        // some code goes here    
        this.tableId = tableid;
        this.tableAlias = tableAlias;
        this.fileIter = Database.getCatalog().getDatabaseFile(tableId).iterator(transactionId);
        this.tupleDesc = this.attachAlias(Database.getCatalog().getTupleDesc(tableid), tableAlias);
        
    }

    public SeqScan(TransactionId tid, int tableid) {
        this(tid, tableid, Database.getCatalog().getTableName(tableid));
    }

    public void open() throws DbException, TransactionAbortedException {
        // some code goes here     
        this.fileIter.open();
    }

    /**
     * Returns the TupleDesc with field names from the underlying HeapFile,
     * prefixed with the tableAlias string from the constructor. This prefix
     * becomes useful when joining tables containing a field(s) with the same
     * name.  The alias and name should be separated with a "." character
     * (e.g., "alias.fieldName").
     *
     * @return the TupleDesc with field names from the underlying HeapFile,
     *         prefixed with the tableAlias string from the constructor.
     */
    public TupleDesc getTupleDesc() {
        // some code goes here     
        return this.tupleDesc;
    }

    public boolean hasNext() throws TransactionAbortedException, DbException {
        // some code goes here   
        if(this.fileIter == null) return false; 
        return this.fileIter.hasNext();
    }

    public Tuple next() throws NoSuchElementException,
            TransactionAbortedException, DbException {
        // some code goes here    
        if(fileIter == null) throw new NoSuchElementException();
        Tuple res = this.fileIter.next();
        if(res == null) throw new NoSuchElementException();
        return res;
    }

    public void close() {
        // some code goes here    
        this.fileIter.close();
    }

    public void rewind() throws DbException, NoSuchElementException,
            TransactionAbortedException {
        // some code goes here     
        this.fileIter.rewind();
    }
}
